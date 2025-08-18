import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { 
  Users, 
  UserPlus, 
  Search, 
  Filter, 
  Download, 
  Upload, 
  Mail,
  Shield,
  AlertTriangle,
  CheckCircle,
  TrendingUp,
  BookOpen,
  Calendar,
  Building,
  Award
} from "lucide-react";
import { apiClient } from "@/lib/api";

const EmployeeManagement = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedDepartment, setSelectedDepartment] = useState("all");
  const [selectedRiskLevel, setSelectedRiskLevel] = useState("all");
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  // Add Employee form state
  const [employeeForm, setEmployeeForm] = useState({
    name: "",
    email: "",
    department: "",
    position: ""
  });

  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        // First, always load from localStorage to ensure we don't lose data
        const savedEmployees = JSON.parse(localStorage.getItem('hopesecure_employees') || '[]');
        let localEmployees = Array.isArray(savedEmployees) ? savedEmployees : [];
        
        // Try to fetch from API 
        try {
          const employeeData = await apiClient.getEmployees();
          const apiEmployees = Array.isArray(employeeData) ? employeeData : ((employeeData as any)?.results || []);
          
          // If API returns data, merge with localStorage (prioritize localStorage for any conflicts)
          if (apiEmployees.length > 0) {
            // Convert API employees to frontend format
            const convertedApiEmployees = apiEmployees.map(emp => ({
              id: emp.id,
              name: `${emp.first_name || ''} ${emp.last_name || ''}`.trim(),
              email: emp.email,
              department: emp.department_name || emp.department,
              position: emp.position || '',
              status: emp.is_active ? 'Active' : 'Inactive',
              riskLevel: emp.risk_level || null,
              riskScore: emp.phishing_susceptibility_score || null,
              trainingPending: 0,
              trainingCompleted: 0,
              vulnerabilityCount: 0,
              lastActivity: emp.last_campaign_date,
              joinDate: emp.hire_date,
              campaignsParticipated: emp.total_campaigns_received || 0,
              hasSimulationResults: emp.total_campaigns_received > 0
            }));
            
            // Merge: keep localStorage employees and add any new API employees
            const mergedEmployees = [...localEmployees];
            convertedApiEmployees.forEach(apiEmp => {
              if (!mergedEmployees.find(localEmp => localEmp.email === apiEmp.email)) {
                mergedEmployees.push(apiEmp);
              }
            });
            setEmployees(mergedEmployees);
          } else {
            // API returned empty, use localStorage
            setEmployees(localEmployees);
          }
        } catch (apiError) {
          console.warn('API fetch failed, using localStorage only:', apiError);
          setEmployees(localEmployees);
        }
      } catch (error) {
        console.error('Error loading employees:', error);
        setEmployees([]);
      } finally {
        setLoading(false);
      }
    };

    fetchEmployees();
  }, []);

  // Handle form input changes
  const handleFormChange = (field: string, value: string) => {
    setEmployeeForm(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Handle add employee
  const handleAddEmployee = async () => {
    if (!employeeForm.name || !employeeForm.email || !employeeForm.department || !employeeForm.position) {
      alert('Please fill in all fields');
      return;
    }

    setIsSubmitting(true);
    try {
      // Split name into first and last name - ensure both are non-empty strings
      const nameParts = employeeForm.name.trim().split(' ');
      const firstName = nameParts[0] || 'Unknown';
      const lastName = nameParts.length > 1 ? nameParts.slice(1).join(' ') : 'Employee';
      
      // Generate employee ID
      const employeeId = `EMP${Date.now()}`;

      // First, try to get departments from API to map name to ID
      let departmentId = null;
      try {
        const departments = await apiClient.getDepartments();
        console.log('Fetched departments:', departments);
        if (Array.isArray(departments)) {
          const department = departments.find(dept => dept.name === employeeForm.department);
          departmentId = department ? department.id : null;
        }
      } catch (deptError) {
        console.warn('Could not fetch departments:', deptError);
      }
      
      // Fallback to static mapping if API fails or no department found
      if (!departmentId) {
        const departmentMapping = {
          'Marketing': 4, 
          'HR': 7,  
          'Finance': 3, 
          'IT': 8, 
          'Sales': 9
        };
        departmentId = departmentMapping[employeeForm.department] || 1;
        console.log(`Using fallback department mapping: ${employeeForm.department} -> ${departmentId}`);
      }

      const backendEmployeeData = {
        employee_id: employeeId,
        first_name: firstName,
        last_name: lastName,
        email: employeeForm.email,
        department: departmentId, // Use the determined department ID
        position: employeeForm.position,
        hire_date: new Date().toISOString().split('T')[0],
        phone_number: '',
        manager_email: '',
        office_location: '',
        security_clearance_level: '',
        has_admin_access: false,
        risk_level: 'medium'
      };

      try {
        // Try API first with correct backend format
        const savedEmployee = await apiClient.createEmployee(backendEmployeeData);
        // Convert backend response to frontend format
        const frontendEmployee = {
          id: savedEmployee.id,
          name: `${savedEmployee.first_name} ${savedEmployee.last_name}`.trim(),
          email: savedEmployee.email,
          department: savedEmployee.department_name || savedEmployee.department,
          position: savedEmployee.position,
          status: savedEmployee.is_active ? 'Active' : 'Inactive',
          riskLevel: null,
          riskScore: null,
          trainingPending: 0,
          trainingCompleted: 0,
          vulnerabilityCount: 0,
          lastActivity: savedEmployee.last_campaign_date,
          joinDate: savedEmployee.hire_date,
          campaignsParticipated: savedEmployee.total_campaigns_received || 0,
          hasSimulationResults: false
        };
        
        // Update state
        const updatedEmployees = Array.isArray(employees) ? [...employees, frontendEmployee] : [frontendEmployee];
        setEmployees(updatedEmployees);
        
        // ALWAYS save to localStorage for persistence
        localStorage.setItem('hopesecure_employees', JSON.stringify(updatedEmployees));
      } catch (apiError) {
        console.warn('API save failed, saving locally:', apiError);
        // Fallback to localStorage - create frontend format data
        const frontendEmployeeData = {
          id: Date.now(),
          name: employeeForm.name,
          email: employeeForm.email,
          department: employeeForm.department,
          position: employeeForm.position,
          status: 'Active',
          riskLevel: null,
          riskScore: null,
          trainingPending: 0,
          trainingCompleted: 0,
          vulnerabilityCount: 0,
          lastActivity: null,
          joinDate: new Date().toISOString().split('T')[0],
          campaignsParticipated: 0,
          hasSimulationResults: false
        };
        const currentEmployees = Array.isArray(employees) ? employees : [];
        const updatedEmployees = [...currentEmployees, frontendEmployeeData];
        setEmployees(updatedEmployees);
        localStorage.setItem('hopesecure_employees', JSON.stringify(updatedEmployees));
      }

      // Reset form and close dialog
      setEmployeeForm({ name: "", email: "", department: "", position: "" });
      setIsDialogOpen(false);
      alert('Employee added successfully!');
    } catch (error) {
      console.error('Error adding employee:', error);
      alert('Failed to add employee. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const departments = ["all", "Marketing", "HR", "Finance", "IT", "Sales"];
  const riskLevels = ["all", "High", "Medium", "Low"];

  // Ensure employees is always an array before filtering
  const employeesArray = Array.isArray(employees) ? employees : [];
  
  const filteredEmployees = employeesArray.filter(employee => {
    const matchesSearch = employee.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         employee.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         employee.department?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDepartment = selectedDepartment === "all" || employee.department === selectedDepartment;
    const matchesRisk = selectedRiskLevel === "all" || employee.riskLevel === selectedRiskLevel;
    return matchesSearch && matchesDepartment && matchesRisk;
  });

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'High': return 'bg-red-100 text-red-800 border-red-200';
      case 'Medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'Low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Active': return 'bg-green-100 text-green-800';
      case 'Training Required': return 'bg-orange-100 text-orange-800';
      case 'Inactive': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  // Calculate department statistics
  const departmentStats = departments.slice(1).map(dept => {
    const deptEmployees = employeesArray.filter(emp => emp.department === dept);
    const highRisk = deptEmployees.filter(emp => emp.riskLevel === 'High').length;
    const employeesWithRiskScores = deptEmployees.filter(emp => emp.riskScore !== null && emp.riskScore !== undefined);
    const avgRisk = employeesWithRiskScores.length > 0 
      ? employeesWithRiskScores.reduce((sum, emp) => sum + (emp.riskScore || 0), 0) / employeesWithRiskScores.length 
      : 0;
    
    return {
      department: dept,
      totalEmployees: deptEmployees.length,
      highRiskCount: highRisk,
      averageRiskScore: Math.round(avgRisk),
      trainingPending: deptEmployees.reduce((sum, emp) => sum + (emp.trainingPending || 0), 0)
    };
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Employee Management</h1>
            <p className="text-gray-600 mt-1">Manage employee security profiles and training</p>
          </div>
          <div className="flex space-x-2">
            <Button variant="outline">
              <Upload className="h-4 w-4 mr-2" />
              Import CSV
            </Button>
            <Button variant="outline">
              <Download className="h-4 w-4 mr-2" />
              Export Report
            </Button>
            <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
              <DialogTrigger asChild>
                <Button>
                  <UserPlus className="h-4 w-4 mr-2" />
                  Add Employee
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Add New Employee</DialogTitle>
                  <DialogDescription>
                    Add a new employee to the security monitoring system
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4 py-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium">Full Name</label>
                      <Input 
                        placeholder="Enter full name" 
                        value={employeeForm.name}
                        onChange={(e) => handleFormChange('name', e.target.value)}
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium">Email Address</label>
                      <Input 
                        placeholder="employee@domain.com" 
                        type="email"
                        value={employeeForm.email}
                        onChange={(e) => handleFormChange('email', e.target.value)}
                      />
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium">Department</label>
                      <Select value={employeeForm.department} onValueChange={(value) => handleFormChange('department', value)}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select department" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem key="Marketing" value="Marketing">Marketing</SelectItem>
                          <SelectItem key="HR" value="HR">HR</SelectItem>
                          <SelectItem key="Finance" value="Finance">Finance</SelectItem>
                          <SelectItem key="IT" value="IT">IT</SelectItem>
                          <SelectItem key="Sales" value="Sales">Sales</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <label className="text-sm font-medium">Position</label>
                      <Input 
                        placeholder="Job title" 
                        value={employeeForm.position}
                        onChange={(e) => handleFormChange('position', e.target.value)}
                      />
                    </div>
                  </div>
                  <div className="flex justify-end space-x-2">
                    <Button variant="outline" onClick={() => setIsDialogOpen(false)}>Cancel</Button>
                    <Button 
                      onClick={handleAddEmployee}
                      disabled={isSubmitting}
                    >
                      {isSubmitting ? 'Adding...' : 'Add Employee'}
                    </Button>
                  </div>
                </div>
              </DialogContent>
            </Dialog>
          </div>
        </div>

        <Tabs defaultValue="employees" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="employees">Employee Directory</TabsTrigger>
            <TabsTrigger value="departments">Department Overview</TabsTrigger>
            <TabsTrigger value="training">Training Progress</TabsTrigger>
          </TabsList>

          <TabsContent value="employees">
            {/* Filters */}
            <Card className="mb-6">
              <CardContent className="p-6">
                <div className="flex flex-col md:flex-row gap-4">
                  <div className="flex-1">
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                      <Input
                        placeholder="Search employees..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="pl-10"
                      />
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <Select value={selectedDepartment} onValueChange={setSelectedDepartment}>
                      <SelectTrigger className="w-48">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {departments.map(dept => (
                          <SelectItem key={dept} value={dept}>
                            {dept === "all" ? "All Departments" : dept}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <Select value={selectedRiskLevel} onValueChange={setSelectedRiskLevel}>
                      <SelectTrigger className="w-40">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {riskLevels.map(risk => (
                          <SelectItem key={risk} value={risk}>
                            {risk === "all" ? "All Risk Levels" : risk}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Employee Table */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Users className="h-5 w-5 mr-2" />
                  Employee Directory ({filteredEmployees.length} employees)
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Employee</TableHead>
                        <TableHead>Department</TableHead>
                        <TableHead>Risk Score</TableHead>
                        <TableHead>Campaigns</TableHead>
                        <TableHead>Vulnerabilities</TableHead>
                        <TableHead>Training</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {filteredEmployees.map((employee) => (
                        <TableRow key={employee.id}>
                          <TableCell>
                            <div>
                              <p className="font-medium">{employee.name}</p>
                              <p className="text-sm text-gray-600">{employee.email}</p>
                              <p className="text-xs text-gray-500">{employee.position}</p>
                            </div>
                          </TableCell>
                          <TableCell>
                            <Badge variant="outline">{employee.department}</Badge>
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center space-x-2">
                              {employee.hasSimulationResults && employee.riskScore !== null ? (
                                <div className="flex items-center space-x-2">
                                  <span className="font-semibold">{employee.riskScore}</span>
                                  <Badge variant="outline" className={getRiskColor(employee.riskLevel)}>
                                    {employee.riskLevel}
                                  </Badge>
                                </div>
                              ) : (
                                <span className="text-gray-400 italic">No simulation data</span>
                              )}
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="text-center">
                              <p className="font-medium">{employee.campaignsParticipated || 0}</p>
                              <p className="text-xs text-gray-500">participated</p>
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center space-x-1">
                              {(employee.vulnerabilityCount || 0) > 0 ? (
                                <AlertTriangle className="h-4 w-4 text-red-500" />
                              ) : (
                                <CheckCircle className="h-4 w-4 text-green-500" />
                              )}
                              <span className={(employee.vulnerabilityCount || 0) > 0 ? "text-red-600 font-medium" : "text-green-600"}>
                                {employee.vulnerabilityCount || 0}
                              </span>
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="text-center">
                              <p className="text-sm">
                                <span className="text-green-600 font-medium">{employee.trainingCompleted || 0}</span>
                                <span className="text-gray-400 mx-1">/</span>
                                <span className="text-orange-600">{employee.trainingPending || 0}</span>
                              </p>
                              <p className="text-xs text-gray-500">completed/pending</p>
                            </div>
                          </TableCell>
                          <TableCell>
                            <Badge className={getStatusColor(employee.status)}>
                              {employee.status}
                            </Badge>
                          </TableCell>
                          <TableCell>
                            <div className="flex space-x-1">
                              <Button key="trend" variant="ghost" size="sm">
                                <TrendingUp className="h-4 w-4" />
                              </Button>
                              <Button key="book" variant="ghost" size="sm">
                                <BookOpen className="h-4 w-4" />
                              </Button>
                              <Button key="mail" variant="ghost" size="sm">
                                <Mail className="h-4 w-4" />
                              </Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="departments">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {departmentStats.map((dept) => (
                <Card key={dept.department}>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span className="flex items-center">
                        <Building className="h-5 w-5 mr-2" />
                        {dept.department}
                      </span>
                      <Badge variant="outline">{dept.totalEmployees} employees</Badge>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <div className="text-center p-3 bg-red-50 rounded-lg">
                          <p className="text-2xl font-bold text-red-600">{dept.highRiskCount}</p>
                          <p className="text-sm text-red-700">High Risk</p>
                        </div>
                        <div className="text-center p-3 bg-blue-50 rounded-lg">
                          <p className="text-2xl font-bold text-blue-600">{dept.averageRiskScore}</p>
                          <p className="text-sm text-blue-700">Avg Risk Score</p>
                        </div>
                      </div>
                      <div className="text-center p-3 bg-orange-50 rounded-lg">
                        <p className="text-xl font-bold text-orange-600">{dept.trainingPending}</p>
                        <p className="text-sm text-orange-700">Pending Training</p>
                      </div>
                      <Button variant="outline" className="w-full">
                        View Details
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="training">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <BookOpen className="h-5 w-5 mr-2" />
                    Training Overview
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center p-4 bg-green-50 rounded-lg">
                      <div>
                        <p className="font-medium text-green-800">Completed Training</p>
                        <p className="text-sm text-green-600">Security awareness courses</p>
                      </div>
                      <div className="text-2xl font-bold text-green-700">
                        {employees.reduce((sum, emp) => sum + emp.trainingCompleted, 0)}
                      </div>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-orange-50 rounded-lg">
                      <div>
                        <p className="font-medium text-orange-800">Pending Training</p>
                        <p className="text-sm text-orange-600">Assigned but not completed</p>
                      </div>
                      <div className="text-2xl font-bold text-orange-700">
                        {employees.reduce((sum, emp) => sum + emp.trainingPending, 0)}
                      </div>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-red-50 rounded-lg">
                      <div>
                        <p className="font-medium text-red-800">Training Required</p>
                        <p className="text-sm text-red-600">High-risk employees</p>
                      </div>
                      <div className="text-2xl font-bold text-red-700">
                        {employees.filter(emp => emp.riskLevel === 'High').length}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Award className="h-5 w-5 mr-2" />
                    Training Assignments
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {employees.filter(emp => emp.trainingPending > 0).map(employee => (
                      <div key={employee.id} className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <p className="font-medium">{employee.name}</p>
                          <p className="text-sm text-gray-600">{employee.department}</p>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Badge variant="outline" className={getRiskColor(employee.riskLevel)}>
                            {employee.riskLevel}
                          </Badge>
                          <Badge variant="secondary">
                            {employee.trainingPending} pending
                          </Badge>
                          <Button size="sm">Assign</Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default EmployeeManagement;
