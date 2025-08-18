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
