import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';

// Custom hook for dashboard data
export const useDashboardData = () => {
  const [data, setData] = useState({
    stats: null,
    campaigns: [],
    templates: [],
    employees: [],
    loading: true,
    error: null
  });

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [stats, campaigns, templates, employees] = await Promise.all([
          apiClient.getDashboardStats(),
          apiClient.getCampaigns(),
          apiClient.getTemplates(),
          apiClient.getEmployees()
        ]);

        setData({
          stats,
          campaigns: campaigns.slice(0, 5), // Recent campaigns
          templates: templates.slice(0, 5), // Recent templates
          employees: employees.slice(0, 10), // Sample employees
          loading: false,
          error: null
        });
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
        setData(prev => ({
          ...prev,
          loading: false,
          error: error.message
        }));
      }
    };

    fetchDashboardData();
  }, []);

  return data;
};

// Custom hook for templates
export const useTemplates = (filters = {}) => {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getTemplates(filters);
        setTemplates(data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch templates:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTemplates();
  }, [JSON.stringify(filters)]);

  const createTemplate = async (templateData) => {
    try {
      const newTemplate = await apiClient.createTemplate(templateData);
      setTemplates([newTemplate, ...templates]);
      return newTemplate;
    } catch (err) {
      console.error('Failed to create template:', err);
      throw err;
    }
  };

  const updateTemplate = async (id, templateData) => {
    try {
      const updatedTemplate = await apiClient.updateTemplate(id, templateData);
      setTemplates(templates.map(t => t.id === id ? updatedTemplate : t));
      return updatedTemplate;
    } catch (err) {
      console.error('Failed to update template:', err);
      throw err;
    }
  };

  const deleteTemplate = async (id) => {
    try {
      await apiClient.deleteTemplate(id);
      setTemplates(templates.filter(t => t.id !== id));
    } catch (err) {
      console.error('Failed to delete template:', err);
      throw err;
    }
  };

  return {
    templates,
    loading,
    error,
    createTemplate,
    updateTemplate,
    deleteTemplate,
    refetch: async () => {
      try {
        setLoading(true);
        const data = await apiClient.getTemplates(filters);
        setTemplates(data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch templates:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
  };
};

// Custom hook for campaigns
export const useCampaigns = () => {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getCampaigns();
        setCampaigns(data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch campaigns:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCampaigns();
  }, []);

  const createCampaign = async (campaignData) => {
    try {
      const newCampaign = await apiClient.createCampaign(campaignData);
      setCampaigns([newCampaign, ...campaigns]);
      return newCampaign;
    } catch (err) {
      console.error('Failed to create campaign:', err);
      throw err;
    }
  };

  const updateCampaign = async (id, campaignData) => {
    try {
      const updatedCampaign = await apiClient.updateCampaign(id, campaignData);
      setCampaigns(campaigns.map(c => c.id === id ? updatedCampaign : c));
      return updatedCampaign;
    } catch (err) {
      console.error('Failed to update campaign:', err);
      throw err;
    }
  };

  const deleteCampaign = async (id) => {
    try {
      await apiClient.deleteCampaign(id);
      setCampaigns(campaigns.filter(c => c.id !== id));
    } catch (err) {
      console.error('Failed to delete campaign:', err);
      throw err;
    }
  };

  return {
    campaigns,
    loading,
    error,
    createCampaign,
    updateCampaign,
    deleteCampaign,
    refetch: async () => {
      try {
        setLoading(true);
        const data = await apiClient.getCampaigns();
        setCampaigns(data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch campaigns:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
  };
};

// Custom hook for employees
export const useEmployees = () => {
  const [employees, setEmployees] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEmployeeData = async () => {
      try {
        setLoading(true);
        const [employeeData, departmentData] = await Promise.all([
          apiClient.getEmployees(),
          apiClient.getDepartments()
        ]);
        setEmployees(employeeData);
        setDepartments(departmentData);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch employee data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchEmployeeData();
  }, []);

  const createEmployee = async (employeeData) => {
    try {
      const newEmployee = await apiClient.createEmployee(employeeData);
      setEmployees([newEmployee, ...employees]);
      return newEmployee;
    } catch (err) {
      console.error('Failed to create employee:', err);
      throw err;
    }
  };

  const updateEmployee = async (id, employeeData) => {
    try {
      const updatedEmployee = await apiClient.updateEmployee(id, employeeData);
      setEmployees(employees.map(e => e.id === id ? updatedEmployee : e));
      return updatedEmployee;
    } catch (err) {
      console.error('Failed to update employee:', err);
      throw err;
    }
  };

  const deleteEmployee = async (id) => {
    try {
      await apiClient.deleteEmployee(id);
      setEmployees(employees.filter(e => e.id !== id));
    } catch (err) {
      console.error('Failed to delete employee:', err);
      throw err;
    }
  };

  return {
    employees,
    departments,
    loading,
    error,
    createEmployee,
    updateEmployee,
    deleteEmployee,
    refetch: async () => {
      try {
        setLoading(true);
        const [employeeData, departmentData] = await Promise.all([
          apiClient.getEmployees(),
          apiClient.getDepartments()
        ]);
        setEmployees(employeeData);
        setDepartments(departmentData);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch employee data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
  };
};
