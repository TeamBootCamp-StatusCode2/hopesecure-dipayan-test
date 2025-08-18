import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "@/contexts/AuthContext";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import Index from "./pages/Index";
import Dashboard from "./pages/Dashboard";
import CreateCampaign from "./pages/CreateCampaign";
import CampaignExecution from "./pages/CampaignExecution";
import TemplateManagement from "./pages/TemplateManagement";
import EmployeeManagement from "./pages/EmployeeManagement";
import AdvancedReports from "./pages/AdvancedReports";
import SettingsPage from "./pages/SettingsPage";
import NotFound from "./pages/NotFound";
import Signin from "./pages/signin"; 
import Signup from "./pages/signup";


const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<Index />} />
            <Route path="/signin" element={<Signin />} />
            <Route path="/signup" element={<Signup />} />
            
            {/* Protected Routes */}
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } />
            <Route path="/campaign/create" element={
              <ProtectedRoute roles={['admin', 'manager', 'analyst']}>
                <CreateCampaign />
              </ProtectedRoute>
            } />
            <Route path="/campaign/execute" element={
              <ProtectedRoute roles={['admin', 'manager', 'analyst']}>
                <CampaignExecution />
              </ProtectedRoute>
            } />
            <Route path="/templates" element={
              <ProtectedRoute roles={['admin', 'manager', 'analyst']}>
                <TemplateManagement />
              </ProtectedRoute>
            } />
            <Route path="/employees" element={
              <ProtectedRoute roles={['admin', 'manager']}>
                <EmployeeManagement />
              </ProtectedRoute>
            } />
            <Route path="/reports" element={
              <ProtectedRoute roles={['admin', 'manager', 'analyst']}>
                <AdvancedReports />
              </ProtectedRoute>
            } />
            <Route path="/settings" element={
              <ProtectedRoute>
                <SettingsPage />
              </ProtectedRoute>
            } />
            
            {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
