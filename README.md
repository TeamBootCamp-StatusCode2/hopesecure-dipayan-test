# 📁 CyberGuard Project - Complete File Structure Guide

> **Target:** Cybersecurity Simulation Platform  
> **Stack:** React + TypeScript (Frontend) + Django REST API (Backend)  
> **Database:** SQLite (Development) / PostgreSQL (Production)  
> **Status:** ✅ Fully Functional & Production Ready

---

## 🏗️ **Root Project Structure**

```
statuscode-backup/                          # 📁 Main Project Root
├── 📄 package.json                         # Frontend dependencies & scripts
├── 📄 vite.config.ts                       # Vite build configuration
├── 📄 tailwind.config.ts                   # Tailwind CSS configuration
├── 📄 tsconfig.json                        # TypeScript main config
├── 📄 tsconfig.app.json                    # TypeScript app config
├── 📄 tsconfig.node.json                   # TypeScript Node.js config
├── 📄 eslint.config.js                     # ESLint configuration
├── 📄 postcss.config.js                    # PostCSS configuration
├── 📄 components.json                      # shadcn/ui components config
├── 📄 index.html                           # Main HTML entry point
├── 📄 bun.lockb                            # Lock file for dependencies
│
├── 📁 src/                                 # 🎯 FRONTEND SOURCE CODE
├── 📁 backend/                             # 🎯 BACKEND SOURCE CODE
├── 📁 public/                              # Static frontend assets
├── 📁 dist/                                # Production build output
│
└── 📄 Documentation Files:
    ├── README.md                           # Project overview
    ├── PROJECT_OVERVIEW.md                 # Detailed project guide
    ├── INTEGRATION_COMPLETE.md             # Integration status
    ├── REAL_TIME_FEATURES.md               # Real-time features info
    ├── PRODUCTION_SECURITY.md              # Production security guide
    └── project_tracker.md                  # Development tracker
```

---

## 🎨 **Frontend Structure (src/)**

### **Main Application Files**
```
src/
├── 📄 main.tsx                            # React app entry point
├── 📄 App.tsx                             # Main App component with routing
├── 📄 App.css                             # Global app styles
├── 📄 index.css                           # Global CSS imports
└── 📄 vite-env.d.ts                       # Vite environment types
```

### **Components Architecture**
```
src/components/
├── 📄 Header.tsx                          # Main navigation header
├── 📄 HeroSection.tsx                     # Landing page hero section
├── 📄 FeaturesSection.tsx                 # Features showcase
├── 📄 HowItWorksSection.tsx               # How it works section
├── 📄 DashboardHeader.tsx                 # Authenticated user header
├── 📄 ProtectedRoute.tsx                  # Route protection wrapper
│
└── 📁 ui/                                 # 🔧 shadcn/ui Components
    ├── 📄 button.tsx                      # Button variants
    ├── 📄 input.tsx                       # Input field
    ├── 📄 badge.tsx                       # Status badges
    ├── 📄 card.tsx                        # Card container
    ├── 📄 dialog.tsx                      # Modal dialogs
    ├── 📄 dropdown-menu.tsx               # Dropdown menus
    ├── 📄 form.tsx                        # Form components
    ├── 📄 label.tsx                       # Form labels
    ├── 📄 select.tsx                      # Select dropdowns
    ├── 📄 table.tsx                       # Data tables
    ├── 📄 tabs.tsx                        # Tab navigation
    ├── 📄 textarea.tsx                    # Text areas
    ├── 📄 toast.tsx                       # Toast notifications
    ├── 📄 toaster.tsx                     # Toast container
    ├── 📄 sonner.tsx                      # Sonner toast system
    ├── 📄 tooltip.tsx                     # Tooltips
    ├── 📄 command.tsx                     # Command palette
    ├── 📄 navigation-menu.tsx             # Navigation menus
    ├── 📄 sidebar.tsx                     # Sidebar layouts
    ├── 📄 toggle.tsx                      # Toggle switches
    └── 📄 ... (other UI components)
```

### **Page Components**
```
src/pages/
├── 📄 Index.tsx                           # 🏠 Landing/Home page
├── 📄 signin.tsx                          # 🔐 Login page (working)
├── 📄 signin-updated.tsx                  # Updated signin version
├── 📄 signup.tsx                          # 📝 Registration page
├── 📄 Dashboard.tsx                       # 📊 Main dashboard
├── 📄 CreateCampaign.tsx                  # ➕ Campaign creation
├── 📄 CampaignExecution.tsx               # ▶️ Campaign management
├── 📄 TemplateManagement.tsx              # 📧 Template CRUD (main)
├── 📄 TemplateManagement_Working.tsx      # Working template version
├── 📄 TemplateManagement_Clean.tsx        # Clean template version
├── 📄 EmployeeManagement.tsx              # 👥 Employee management
├── 📄 AdvancedReports.tsx                 # 📈 Analytics & reports
├── 📄 PhishingSimulation.tsx              # 🎣 Simulation interface
├── 📄 RealTimeCampaignMonitor.tsx         # 📡 Real-time monitoring
├── 📄 SettingsPage.tsx                    # ⚙️ User settings
└── 📄 NotFound.tsx                        # 404 error page
```

### **Business Logic & State**
```
src/
├── 📁 contexts/
│   └── 📄 AuthContext.tsx                 # 🔐 Authentication state management
│
├── 📁 hooks/
│   ├── 📄 useApi.ts                       # 🔗 API data fetching hooks
│   ├── 📄 use-mobile.tsx                  # 📱 Mobile detection
│   └── 📄 use-toast.ts                    # 🍞 Toast notification hook
│
├── 📁 lib/
│   ├── 📄 api.ts                          # 🌐 Main API client & types
│   └── 📄 utils.ts                        # 🛠️ Utility functions
│
└── 📁 data/
    └── 📄 templates.ts                    # 📋 Static template data
```

### **Static Assets**
```
src/assets/
├── 🖼️ hero-security.jpg                  # Hero section image
├── 🖼️ hopsecurelogo.png                  # Company logo
└── 🖼️ ChatGPT Image Aug 15, 2025...     # AI generated image
```

---

## 🔧 **Backend Structure (backend/)**

### **Django Project Core**
```
backend/
├── 📄 manage.py                           # Django management script
├── 📄 requirements.txt                    # Python dependencies
├── 📄 db.sqlite3                          # SQLite database file
├── 📄 .env                                # Environment variables
├── 📄 datadump.json                       # Sample data export
├── 📄 test_api.py                         # API testing script
│
├── 📄 Documentation:
│   ├── README.md                          # Backend setup guide
│   └── FRONTEND_INTEGRATION.md            # Integration guide
│
└── 📁 Django Apps:                        # Each app handles specific functionality
```

### **Main Django Configuration**
```
backend/cyberguard_backend/
├── 📄 __init__.py                         # Python package marker
├── 📄 settings.py                         # 🔧 Django settings (MAIN CONFIG)
├── 📄 urls.py                             # URL routing configuration
├── 📄 wsgi.py                             # WSGI server interface
├── 📄 asgi.py                             # ASGI server interface
└── 📁 __pycache__/                        # Python bytecode cache
```

### **Authentication App**
```
backend/authentication/
├── 📄 __init__.py                         # App package marker
├── 📄 apps.py                             # App configuration
├── 📄 admin.py                            # Django admin interface
├── 📄 models.py                           # 👤 User model & database schema
├── 📄 serializers.py                     # 📦 API data serialization
├── 📄 views.py                            # 🎯 API endpoints logic
├── 📄 urls.py                             # App URL routing
├── 📄 tests.py                            # Unit tests
├── 📁 migrations/                         # Database migration files
│   ├── 📄 0001_initial.py                # Initial user model migration
│   └── 📄 __init__.py
└── 📁 __pycache__/                        # Python bytecode cache
```

### **Templates App**
```
backend/templates/
├── 📄 models.py                           # 📧 Email template models
├── 📄 serializers.py                     # Template API serialization
├── 📄 views.py                            # Template CRUD endpoints
├── 📄 urls.py                             # Template routing
├── 📄 admin.py                            # Admin interface
├── 📄 tests.py                            # Template tests
├── 📁 migrations/                         # Database migrations
│   └── 📄 0001_initial.py                # Template schema migration
├── 📁 management/                         # Management commands
│   └── 📁 commands/
│       └── 📄 populate_sample_data.py    # Sample data loader
└── 📁 __pycache__/
```

### **Campaigns App**
```
backend/campaigns/
├── 📄 models.py                           # 🎯 Campaign models & targets
├── 📄 serializers.py                     # Campaign API serialization
├── 📄 views.py                            # Campaign management endpoints
├── 📄 urls.py                             # Campaign routing
├── 📄 admin.py                            # Campaign admin interface
├── 📄 tests.py                            # Campaign tests
├── 📁 migrations/
│   └── 📄 0001_initial.py
└── 📁 __pycache__/
```

### **Employees App**
```
backend/employees/
├── 📄 models.py                           # 👥 Employee & Department models
├── 📄 serializers.py                     # Employee API serialization
├── 📄 views.py                            # Employee management endpoints
├── 📄 urls.py                             # Employee routing
├── 📄 admin.py                            # Employee admin
├── 📄 tests.py                            # Employee tests
├── 📁 migrations/
│   └── 📄 0001_initial.py
└── 📁 __pycache__/
```

### **Reports App**
```
backend/reports/
├── 📄 models.py                           # 📊 Analytics & reporting models
├── 📄 serializers.py                     # Reports API serialization
├── 📄 views.py                            # Analytics endpoints
├── 📄 urls.py                             # Reports routing
├── 📄 admin.py                            # Reports admin
├── 📄 tests.py                            # Reports tests
├── 📁 migrations/
│   └── 📄 0001_initial.py
└── 📁 __pycache__/
```

---

## 🗄️ **Database Schema Overview**

### **Core Models & Relationships**
```
📊 Database Structure:

authentication.User                         # Extended Django user
├── id, email, username, password
├── first_name, last_name, role
├── department, phone_number
└── is_email_verified, created_at

employees.Department                        # Organizational structure
├── id, name, description
├── manager (ForeignKey to User)
└── created_at

employees.Employee                          # Employee profiles
├── id, employee_id, first_name, last_name
├── email, department (ForeignKey)
├── position, phone_number, hire_date
├── security_level, vulnerability_score
└── is_active, created_at

templates.Template                          # Phishing email templates
├── id, name, category, description
├── email_subject, sender_name, sender_email
├── html_content, css_styles
├── landing_page_url, domain
├── difficulty, risk_level, status
├── tracking_enabled, created_by
└── usage_count, success_rate, rating

campaigns.Campaign                          # Phishing campaigns
├── id, name, description
├── template (ForeignKey to Template)
├── status, start_date, end_date
├── target_count, targets_sent
├── email_opened, links_clicked
├── credentials_submitted
└── created_by, created_at

reports.Report                              # Analytics & reports
├── id, campaign (ForeignKey)
├── report_type, generated_at
├── data (JSON field)
└── created_by
```

---

## 🌐 **API Endpoints Structure**

### **Authentication Endpoints**
```
🔐 /api/auth/
├── POST /login/                           # User authentication
├── POST /logout/                          # User logout
├── POST /register/                        # User registration
├── GET  /profile/                         # User profile
├── PUT  /profile/update/                  # Update profile
└── GET  /dashboard/stats/                 # Dashboard statistics
```

### **Templates Endpoints**
```
📧 /api/templates/
├── GET    /                               # List all templates
├── POST   /                               # Create new template
├── GET    /{id}/                          # Get template details
├── PUT    /{id}/                          # Update template
├── DELETE /{id}/                          # Delete template
├── POST   /{id}/clone/                    # Clone template
└── GET    /{id}/preview/                  # Preview template
```

### **Campaigns Endpoints**
```
🎯 /api/campaigns/
├── GET    /                               # List all campaigns
├── POST   /                               # Create new campaign
├── GET    /{id}/                          # Get campaign details
├── PUT    /{id}/                          # Update campaign
├── DELETE /{id}/                          # Delete campaign
├── POST   /{id}/start/                    # Start campaign
└── POST   /{id}/pause/                    # Pause campaign
```

### **Employees Endpoints**
```
👥 /api/employees/
├── GET    /                               # List all employees
├── POST   /                               # Create new employee
├── GET    /{id}/                          # Get employee details
├── PUT    /{id}/                          # Update employee
├── DELETE /{id}/                          # Delete employee
└── GET    /departments/                   # List departments
```

---

## 📦 **Key Dependencies**

### **Frontend Dependencies (package.json)**
```json
{
  "dependencies": {
    "react": "^18.3.1",                    // Core React framework
    "react-dom": "^18.3.1",               // React DOM renderer
    "react-router-dom": "^6.30.1",        // Client-side routing
    "@tanstack/react-query": "^5.83.0",   // Server state management
    "tailwindcss": "^3.4.17",             // CSS framework
    "@radix-ui/react-*": "...",           // UI component library
    "typescript": "^5.8.3",               // Type safety
    "vite": "^5.4.19",                    // Build tool
    "lucide-react": "^0.462.0"            // Icon library
  }
}
```

### **Backend Dependencies (requirements.txt)**
```txt
Django==5.2.5                             # Web framework
djangorestframework==3.15.2               # REST API framework
django-cors-headers==4.4.0                # CORS handling
Pillow==10.4.0                            # Image processing
psycopg2-binary==2.9.10                   # PostgreSQL adapter
```

---

## 🚀 **Development Workflow**

### **Starting the Application**
```bash
# Terminal 1: Backend Server
cd backend
python manage.py runserver                # Runs on http://127.0.0.1:8000

# Terminal 2: Frontend Server  
npm run dev                                # Runs on http://localhost:8081
```

### **Available Scripts**
```bash
# Frontend Commands
npm run dev          # Start development server
npm run build        # Build for production  
npm run preview      # Preview production build
npm run lint         # Run ESLint

# Backend Commands
python manage.py runserver              # Start Django server
python manage.py migrate               # Apply database migrations
python manage.py createsuperuser       # Create admin user
python manage.py populate_sample_data  # Load sample data
python manage.py test                  # Run tests
```

---

## 🔒 **Security & Configuration**

### **Important Configuration Files**
```
🔧 Key Config Files:
├── backend/cyberguard_backend/settings.py    # Django settings
├── backend/.env                               # Environment variables
├── vite.config.ts                            # Vite configuration
├── tailwind.config.ts                        # Tailwind CSS config
└── tsconfig.json                             # TypeScript config
```

### **Environment Variables (.env)**
```bash
DEBUG=True                                 # Development mode
SECRET_KEY=django-insecure-...             # Django secret key
DATABASE_URL=sqlite:///db.sqlite3          # Database connection
ALLOWED_HOSTS=localhost,127.0.0.1          # Allowed hosts
CORS_ALLOWED_ORIGINS=http://localhost:8081 # CORS origins
```

---

## 📋 **Project Status & Features**

### **✅ Completed Features**
- ✅ User Authentication (Login/Logout)
- ✅ Protected Routes with Role-Based Access
- ✅ Dashboard with Real Data
- ✅ Template Management (CRUD)
- ✅ Campaign Management
- ✅ Employee Management
- ✅ REST API Backend
- ✅ Frontend-Backend Integration
- ✅ Responsive UI Design
- ✅ Production Build Ready

### **🎯 Core User Roles**
- **Admin:** Full system access
- **Manager:** Campaign & employee management
- **Analyst:** Template creation & campaign execution
- **Employee:** Limited access to personal data

---

## 🚧 **Development Notes for Team**

### **Important File Interactions**
1. **Authentication Flow:** `AuthContext.tsx` ↔ `api.ts` ↔ `authentication/views.py`
2. **Routing:** `App.tsx` → `pages/*.tsx` → Protected by `ProtectedRoute.tsx`
3. **API Communication:** `hooks/useApi.ts` → `lib/api.ts` → Django REST endpoints
4. **Database:** Django Models → Migrations → SQLite/PostgreSQL

### **Code Organization Principles**
- **Frontend:** Component-based architecture with hooks for state
- **Backend:** Django apps for feature separation
- **API:** RESTful design with DRF serializers
- **Styling:** Tailwind CSS with shadcn/ui components
- **Type Safety:** TypeScript throughout frontend

### **Development Best Practices**
- Always test in both dev and build modes
- Use TypeScript interfaces for API responses
- Follow Django REST framework conventions
- Maintain consistent file naming
- Document new features and API changes

---

## 📞 **For Team Questions**

**Frontend Issues:** Check `src/` structure, API integration in `lib/api.ts`  
**Backend Issues:** Check Django apps in `backend/`, settings in `settings.py`  
**Database Issues:** Check models and migrations in each app  
**Build Issues:** Check `vite.config.ts`, `package.json`, and TypeScript configs  

**Current Status:** ✅ Fully functional development and production environment!
