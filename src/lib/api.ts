// Simple API client for React frontend
export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  full_name: string;
  role: string;
  department: string;
  phone_number: string;
  is_email_verified: boolean;
  created_at: string;
}

export interface Company {
  id: number;
  name: string;
  domain: string;
  industry: string;
  employee_count: string;
  address: string;
  phone: string;
  website: string;
  registration_number: string;
  founded_year: string;
  timezone: string;
  language: string;
  logo?: string;
  created_at: string;
  updated_at: string;
}

export interface Template {
  id: number;
  name: string;
  category: string;
  description: string;
  email_subject: string;
  sender_name: string;
  sender_email: string;
  html_content: string;
  css_styles?: string;
  landing_page_url?: string;
  domain: string;
  difficulty: string;
  risk_level: string;
  status: string;
  has_attachments: boolean;
  has_css: boolean;
  is_responsive: boolean;
  usage_count: number;
  success_rate: string;
  rating: number;
  tracking_enabled: boolean;
  priority: string;
  created_by: number;
  created_at: string;
  updated_at: string;
  last_used?: string;
}

const API_BASE_URL = "http://127.0.0.1:8000/api";

class APIClient {
  private token: string | null = localStorage.getItem("auth_token");

  async login(email: string, password: string) {
    const response = await fetch(`${API_BASE_URL}/auth/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    this.token = data.token;
    localStorage.setItem("auth_token", data.token);
    return data;
  }

  async register(userData: any) {
    const response = await fetch(`${API_BASE_URL}/auth/register/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || 'Registration failed');
    }
    if (data.token) {
      this.token = data.token;
      localStorage.setItem("auth_token", data.token);
    }
    return data;
  }

  async logout() {
    if (this.token) {
      await fetch(`${API_BASE_URL}/auth/logout/`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Token ${this.token}`
        },
      });
    }
    this.token = null;
    localStorage.removeItem("auth_token");
  }

  async getProfile(): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/profile/`, {
      headers: { "Authorization": `Token ${this.token}` },
    });
    if (!response.ok) {
      throw new Error('Failed to fetch user profile');
    }
    return response.json();
  }

  async getCompanyInfo(): Promise<Company> {
    const response = await fetch(`${API_BASE_URL}/organization/company/`, {
      headers: { "Authorization": `Token ${this.token}` },
    });
    if (!response.ok) {
      throw new Error('Failed to fetch company information');
    }
    return response.json();
  }

  async updateCompanyInfo(companyData: Partial<Company>): Promise<Company> {
    const response = await fetch(`${API_BASE_URL}/organization/company/update/`, {
      method: "PUT",
      headers: { 
        "Content-Type": "application/json",
        "Authorization": `Token ${this.token}`
      },
      body: JSON.stringify(companyData),
    });
    const data = await response.json();
    if (!response.ok) {
      // Log the actual error details for debugging
      console.error('Update company error:', data);
      throw new Error(data.error || JSON.stringify(data) || 'Failed to update company information');
    }
    return data;
  }

  async uploadCompanyLogo(logoFile: File): Promise<Company> {
    const formData = new FormData();
    formData.append('logo', logoFile);

    const response = await fetch(`${API_BASE_URL}/organization/company/upload-logo/`, {
      method: "POST",
      headers: { 
        "Authorization": `Token ${this.token}`
      },
      body: formData,
    });
    const data = await response.json();
    if (!response.ok) {
      console.error('Upload logo error:', data);
      throw new Error(data.error || 'Failed to upload logo');
    }
    return data;
  }

  // Template API methods
  async getTemplates(): Promise<Template[]> {
    const response = await fetch(`${API_BASE_URL}/templates/`, {
      method: "GET",
      headers: { 
        "Authorization": `Token ${this.token}`
      },
    });
    const data = await response.json();
    if (!response.ok) {
      console.error('Get templates error:', data);
      throw new Error(data.error || 'Failed to fetch templates');
    }
    // Handle paginated response - return results array or the data if it's already an array
    return Array.isArray(data) ? data : (data.results || []);
  }

  async createTemplate(templateData: Partial<Template>): Promise<Template> {
    const headers: Record<string, string> = { 
      "Content-Type": "application/json"
    };
    
    // Only add authorization if token exists
    if (this.token) {
      headers["Authorization"] = `Token ${this.token}`;
    }
    
    const response = await fetch(`${API_BASE_URL}/templates/`, {
      method: "POST",
      headers,
      body: JSON.stringify(templateData),
    });
    const data = await response.json();
    if (!response.ok) {
      console.error('Create template error:', data);
      console.error('Response status:', response.status);
      console.error('Request data:', templateData);
      throw new Error(data.detail || data.error || JSON.stringify(data) || 'Failed to create template');
    }
    return data;
  }

  async updateTemplate(id: number, templateData: Partial<Template>): Promise<Template> {
    const response = await fetch(`${API_BASE_URL}/templates/${id}/`, {
      method: "PUT",
      headers: { 
        "Content-Type": "application/json",
        "Authorization": `Token ${this.token}`
      },
      body: JSON.stringify(templateData),
    });
    const data = await response.json();
    if (!response.ok) {
      console.error('Update template error:', data);
      throw new Error(data.error || 'Failed to update template');
    }
    return data;
  }

  async deleteTemplate(id: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/templates/${id}/`, {
      method: "DELETE",
      headers: { 
        "Authorization": `Token ${this.token}`
      },
    });
    if (!response.ok) {
      const data = await response.json();
      console.error('Delete template error:', data);
      throw new Error(data.error || 'Failed to delete template');
    }
  }

  async cloneTemplate(id: number): Promise<Template> {
    const response = await fetch(`${API_BASE_URL}/templates/${id}/clone/`, {
      method: "POST",
      headers: { 
        "Authorization": `Token ${this.token}`
      },
    });
    const data = await response.json();
    if (!response.ok) {
      console.error('Clone template error:', data);
      throw new Error(data.error || 'Failed to clone template');
    }
    return data;
  }

  // Campaign API methods
  async getCampaigns(): Promise<any[]> {
    const response = await fetch(`${API_BASE_URL}/campaigns/`, {
      method: "GET",
      headers: { 
        "Authorization": `Token ${this.token}`
      },
    });
    const data = await response.json();
    if (!response.ok) {
      console.error('Get campaigns error:', data);
      throw new Error(data.error || 'Failed to fetch campaigns');
    }
    return data;
  }

  async createCampaign(campaignData: any): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/campaigns/`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Authorization": `Token ${this.token}`
      },
      body: JSON.stringify(campaignData),
    });
    const data = await response.json();
    if (!response.ok) {
      console.error('Create campaign error:', data);
      throw new Error(data.error || 'Failed to create campaign');
    }
    return data;
  }

  // Employee API methods
  async getEmployees(): Promise<any[]> {
    const response = await fetch(`${API_BASE_URL}/employees/`, {
      method: "GET",
      headers: { 
        "Authorization": `Token ${this.token}`
      },
    });
    const data = await response.json();
    if (!response.ok) {
      console.error('Get employees error:', data);
      throw new Error(data.error || 'Failed to fetch employees');
    }
    return data.results || data; // Return the results array, or data if it's already an array
  }

  async createEmployee(employeeData: any): Promise<any> {
    console.log('Creating employee with data:', employeeData);
    const response = await fetch(`${API_BASE_URL}/employees/`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Authorization": `Token ${this.token}`
      },
      body: JSON.stringify(employeeData),
    });
    
    const data = await response.json();
    if (!response.ok) {
      console.error('Create employee error:', data);
      console.error('Response status:', response.status, response.statusText);
      throw new Error(JSON.stringify(data) || 'Failed to create employee');
    }
    return data;
  }

  async getDepartments(): Promise<any[]> {
    const response = await fetch(`${API_BASE_URL}/employees/departments/`, {
      method: "GET",
      headers: { 
        "Authorization": `Token ${this.token}`
      },
    });
    
    if (!response.ok) {
      console.error(`Departments API error: ${response.status} ${response.statusText}`);
      const text = await response.text();
      console.error('Response text:', text);
      throw new Error(`Failed to fetch departments: ${response.status}`);
    }
    
    const data = await response.json();
    return data.results || data; // Return the results array, or data if it's already an array
  }

  getToken() {
    return this.token;
  }

  setToken(token: string) {
    this.token = token;
    localStorage.setItem("auth_token", token);
  }

  clearToken() {
    this.token = null;
    localStorage.removeItem("auth_token");
  }
}

export const apiClient = new APIClient();

export const setUserData = (user: User) => {
  localStorage.setItem("user_data", JSON.stringify(user));
};

export const clearUserData = () => {
  localStorage.removeItem("user_data");
};
