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
    return response.json();
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
