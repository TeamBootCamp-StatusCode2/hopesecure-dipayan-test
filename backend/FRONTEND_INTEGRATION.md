# Frontend Integration Guide

This guide explains how to integrate your React frontend with the Django backend API.

## 🔗 Backend API Base URL

The Django backend is running at: `http://127.0.0.1:8000/api`

## 🛠️ Frontend Setup

### 1. Update Your Frontend API Configuration

Create or update your API configuration file (e.g., `src/lib/api.ts`):

```typescript
// src/lib/api.ts
const API_BASE_URL = 'http://127.0.0.1:8000/api';

export const apiConfig = {
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
};

// API client with authentication
export class ApiClient {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
    this.token = localStorage.getItem('auth_token');
  }

  setToken(token: string) {
    this.token = token;
    localStorage.setItem('auth_token', token);
  }

  clearToken() {
    this.token = null;
    localStorage.removeItem('auth_token');
  }

  private getHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Token ${this.token}`;
    }

    return headers;
  }

  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const config: RequestInit = {
      ...options,
      headers: {
        ...this.getHeaders(),
        ...options.headers,
      },
    };

    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }

    return response.json();
  }

  // Auth methods
  async login(email: string, password: string) {
    const response = await this.request<{user: any, token: string}>('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    
    this.setToken(response.token);
    return response;
  }

  async register(userData: any) {
    const response = await this.request<{user: any, token: string}>('/auth/register/', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
    
    this.setToken(response.token);
    return response;
  }

  async logout() {
    await this.request('/auth/logout/', { method: 'POST' });
    this.clearToken();
  }

  // Templates
  async getTemplates() {
    return this.request<any[]>('/templates/');
  }

  async getTemplate(id: number) {
    return this.request<any>(`/templates/${id}/`);
  }

  async createTemplate(templateData: any) {
    return this.request<any>('/templates/', {
      method: 'POST',
      body: JSON.stringify(templateData),
    });
  }

  // Campaigns
  async getCampaigns() {
    return this.request<any[]>('/campaigns/');
  }

  async getCampaign(id: number) {
    return this.request<any>(`/campaigns/${id}/`);
  }

  async createCampaign(campaignData: any) {
    return this.request<any>('/campaigns/', {
      method: 'POST',
      body: JSON.stringify(campaignData),
    });
  }

  // Employees
  async getEmployees() {
    return this.request<any[]>('/employees/');
  }

  async getEmployee(id: number) {
    return this.request<any>(`/employees/${id}/`);
  }

  // Dashboard
  async getDashboardStats() {
    return this.request<any>('/auth/dashboard/stats/');
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
```

### 2. Update Authentication Pages

Update your sign-in and sign-up components to use the real API:

```typescript
// src/pages/signin.tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '@/lib/api';

export default function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await apiClient.login(email, password);
      console.log('Login successful:', response);
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  // ... rest of component
}
```

### 3. Update Dashboard with Real Data

```typescript
// src/pages/Dashboard.tsx
import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null);
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [dashboardStats, campaignsList] = await Promise.all([
          apiClient.getDashboardStats(),
          apiClient.getCampaigns(),
        ]);
        
        setStats(dashboardStats);
        setCampaigns(campaignsList);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  // ... rest of component using real data
}
```

### 4. Update Template Management

```typescript
// src/pages/TemplateManagement.tsx
import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';

export default function TemplateManagement() {
  const [templates, setTemplates] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        const templatesList = await apiClient.getTemplates();
        setTemplates(templatesList);
      } catch (error) {
        console.error('Failed to fetch templates:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTemplates();
  }, []);

  const handleCreateTemplate = async (templateData: any) => {
    try {
      const newTemplate = await apiClient.createTemplate(templateData);
      setTemplates([...templates, newTemplate]);
    } catch (error) {
      console.error('Failed to create template:', error);
    }
  };

  // ... rest of component
}
```

## 🔐 Authentication Flow

### 1. Login Process
1. User enters credentials
2. Frontend sends POST to `/api/auth/login/`
3. Backend returns user data and token
4. Frontend stores token in localStorage
5. Frontend includes token in all subsequent requests

### 2. Protected Routes
```typescript
// src/components/ProtectedRoute.tsx
import { Navigate } from 'react-router-dom';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const token = localStorage.getItem('auth_token');
  
  if (!token) {
    return <Navigate to="/signin" replace />;
  }
  
  return <>{children}</>;
}
```

### 3. Update App Routes
```typescript
// src/App.tsx
import { ProtectedRoute } from '@/components/ProtectedRoute';

function App() {
  return (
    <Routes>
      <Route path="/signin" element={<SignIn />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      } />
      {/* ... other protected routes */}
    </Routes>
  );
}
```

## 📊 Data Integration

### Replace Static Data

Update your data files to use API data:

```typescript
// Instead of static data in src/data/templates.ts
export const useTemplates = () => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        const data = await apiClient.getTemplates();
        setTemplates(data);
      } catch (error) {
        console.error('Failed to fetch templates:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTemplates();
  }, []);

  return { templates, loading, setTemplates };
};
```

## 🔄 Real-time Updates

For real-time features, you can implement polling or WebSockets:

```typescript
// Simple polling example
export const useCampaignStats = (campaignId: number) => {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await apiClient.getCampaign(campaignId);
        setStats(data);
      } catch (error) {
        console.error('Failed to fetch campaign stats:', error);
      }
    };

    fetchStats();
    const interval = setInterval(fetchStats, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, [campaignId]);

  return stats;
};
```

## 🚀 Testing Integration

### Test with Sample Accounts

Use these test accounts that were created with sample data:

```
Admin Account:
- Email: admin@cyberguard.com
- Password: (the one you set when creating superuser)

Manager Account:
- Email: manager@cyberguard.com
- Password: password123

Analyst Account:
- Email: analyst@cyberguard.com
- Password: password123
```

### Verify API Endpoints

Test each endpoint in your browser or with curl:

```bash
# Test login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "manager@cyberguard.com", "password": "password123"}'

# Test templates (use token from login response)
curl -H "Authorization: Token YOUR_TOKEN_HERE" \
  http://127.0.0.1:8000/api/templates/
```

## 🐛 Common Issues

### CORS Errors
- Ensure your frontend URL is in `CORS_ALLOWED_ORIGINS` in Django settings
- Check browser console for CORS-related errors

### Authentication Errors
- Verify token format: `Token your_token_here`
- Check if token is expired or invalid
- Ensure token is included in request headers

### API Errors
- Check Django server logs for detailed error messages
- Verify request payload format matches expected schema
- Check HTTP status codes for error types

## 📱 Mobile/Responsive Considerations

The backend API is designed to work with any frontend, including mobile apps. For React Native or mobile web:

- Use the same API endpoints
- Handle authentication tokens in secure storage
- Consider offline capabilities with local data caching

## 🔧 Development Tips

1. **Use environment variables** for API URLs
2. **Implement error boundaries** for API failures
3. **Add loading states** for better UX
4. **Cache API responses** when appropriate
5. **Handle network errors** gracefully

## 📈 Next Steps

1. **Start with authentication** - Get login/logout working first
2. **Add dashboard integration** - Connect real data to dashboard
3. **Implement CRUD operations** - Templates, campaigns, employees
4. **Add error handling** - Proper error states and messages
5. **Optimize performance** - Caching, pagination, lazy loading

Your Django backend is now ready for integration! The API provides all the functionality needed to replace the static data in your React frontend with real, dynamic data.
