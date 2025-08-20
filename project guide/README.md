# 📁 HopeSecure Project - Complete Guide & Documentation

> **Target:** Advanced Cybersecurity Awareness Platform  
> **Stack:** React + TypeScript (Frontend) + Django REST API (Backend)  
> **Database:** SQLite (Development) / PostgreSQL (Production)  
> **Status:** ✅ Production Ready with Real-Time Features  
> **Updated:** August 2025

---

## 🏗️ **Current Project Structure**

```
hopesecure-dipayan-test/                    # 📁 Main Project Root
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
├── 📄 clear_storage.js                     # Development utility
├── 📄 clear_user_templates.js              # Development utility
├── 📄 debug_session.html                   # Debug interface
│
├── 📁 src/                                 # 🎯 FRONTEND SOURCE CODE
├── 📁 backend/                             # 🎯 BACKEND SOURCE CODE
├── 📁 public/                              # Static frontend assets
├── 📁 project guide/                       # 📚 ALL PROJECT DOCUMENTATION
│
└── 📄 Legacy Documentation (moved to project guide/):
    ├── All .md files now organized in project guide folder
    └── Comprehensive documentation structure
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
├── 📄 CampaignNotification.tsx            # Real-time campaign notifications
├── 📄 LogoutButton.tsx                    # Logout functionality
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
    ├── 📄 checkbox.tsx                    # Checkbox components
    ├── 📄 switch.tsx                      # Switch toggles
    └── 📄 ... (other UI components)
```

### **Page Components**
```
src/pages/
├── 📄 Index.tsx                           # 🏠 Landing/Home page
├── 📄 signin.tsx                          # 🔐 Login page (current)
├── 📄 signin-updated.tsx                  # Updated signin version
├── 📄 signup.tsx                          # 📝 Registration page
├── 📄 Dashboard.tsx                       # 📊 Main dashboard with CRUD operations
├── 📄 CreateCampaign.tsx                  # ➕ Campaign creation & editing
├── 📄 CampaignExecution.tsx               # ▶️ Real-time campaign monitoring
├── 📄 TemplateManagement.tsx              # 📧 Template CRUD (main)
├── 📄 TemplateManagement_Working.tsx      # Working template version
├── 📄 TemplateManagement_Clean.tsx        # Clean template version
├── 📄 EmployeeManagement.tsx              # 👥 Employee management
├── 📄 AdvancedReports.tsx                 # 📈 Analytics & reports
├── 📄 PhishingSimulation.tsx              # 🎣 Simulation interface
├── 📄 RealTimeCampaignMonitor.tsx         # 📡 Real-time monitoring
├── 📄 SettingsPage.tsx                    # ⚙️ Company management & settings
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
│   ├── 📄 useCampaigns.ts                 # 🎯 Campaign state management
│   ├── 📄 use-mobile.tsx                  # 📱 Mobile detection
│   └── 📄 use-toast.ts                    # 🍞 Toast notification hook
│
├── 📁 lib/
│   ├── 📄 api.ts                          # 🌐 Main API client & types
│   └── 📄 utils.ts                        # 🛠️ Utility functions
│
└── 📁 data/
    └── 📄 templates.ts                    # 📋 Static template data & fallbacks
```

### **Static Assets**
```
src/assets/
├── 🖼️ hero-security.jpg                  # Hero section image
├── 🖼️ hopsecurelogo.png                  # Company logo
└── 🖼️ react.svg                          # React logo

public/
├── 🖼️ favicon.ico                        # Site favicon
├── 🖼️ placeholder.svg                    # Placeholder images
└── 📄 robots.txt                          # SEO robots file
```

---

## 🔧 **Backend Structure (backend/)**

### **Django Project Core**
```
backend/
├── 📄 manage.py                           # Django management script
├── 📄 requirements.txt                    # Python dependencies
├── 📄 db.sqlite3                          # SQLite database file
├── 📄 test_api.py                         # API testing script
├── 📄 verify_setup.py                     # Setup verification
├── 📄 create_sample_admin_data.py         # Sample admin data
├── 📄 create_super_admin.py               # Super admin creation
├── 📄 check_accounts.py                   # Account verification
├── 📄 check_companies.py                  # Company data check
├── 📄 fix_data_ownership.py               # Data ownership fixes
├── 📄 migrate_organizations.py            # Organization migration
│
├── 📁 media/                              # Media files storage
│   └── 📁 company_logos/                  # Company logo uploads
│
├── � Documentation/ (moved to project guide/):
│   ├── BACKEND_README.md                  # Backend setup guide
│   └── FRONTEND_INTEGRATION.md            # Integration guide
│
└── 📁 Django Apps:                        # Each app handles specific functionality
```

### **Main Django Configuration**
```
backend/hopesecure_backend/                # Updated from cyberguard_backend
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

### **Organization App**
```
backend/organization/
├── 📄 models.py                           # 🏢 Organization & company models
├── 📄 serializers.py                     # Organization API serialization
├── 📄 views.py                            # Organization management endpoints
├── 📄 urls.py                             # Organization routing
├── 📄 admin.py                            # Organization admin interface
├── 📄 tests.py                            # Organization tests
├── 📁 migrations/
│   └── 📄 0001_initial.py
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

## � **Project Documentation Structure**

### **Complete Documentation in `project guide/` folder:**
```
project guide/
├── 📄 README.md                           # This comprehensive guide
├── 📄 BACKEND_README.md                   # Backend setup & API guide
├── 📄 FRONTEND_INTEGRATION.md             # Frontend-backend integration
├── 📄 PROJECT_OVERVIEW.md                 # Detailed project overview
├── 📄 PROJECT_FILE_STRUCTURE.md           # File structure details
├── 📄 INTEGRATION_COMPLETE.md             # Integration completion status
├── 📄 REAL_TIME_FEATURES.md               # Real-time functionality docs
├── 📄 PRODUCTION_SECURITY.md              # Production security guide
├── 📄 ADMIN_MONITORING_IMPLEMENTATION.md  # Admin monitoring features
├── 📄 SUPER_ADMIN_IMPLEMENTATION.md       # Super admin functionality
├── 📄 ORGANIZATIONAL_REGISTRATION_IMPLEMENTATION.md # Org registration
├── 📄 SECURITY_MONITORING_ACCESS_UPDATE.md # Security monitoring access
└── 📄 project_tracker.md                  # Development progress tracker
```

---

## �🗄️ **Database Schema Overview**

### **Core Models & Relationships**
```
📊 Database Structure:

authentication.User                         # Extended Django user
├── id, email, username, password
├── first_name, last_name, role
├── department, phone_number
└── is_email_verified, created_at

organization.Organization                   # Company/organization data
├── id, name, domain, industry
├── employee_count, timezone
├── company_address, website_url
├── phone_number, registration_number
├── founded_year, default_language
└── created_at, updated_at

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

### **Organization Endpoints**
```
🏢 /api/organization/
├── GET    /                               # List organizations
├── POST   /                               # Create organization
├── GET    /{id}/                          # Get organization details
├── PUT    /{id}/                          # Update organization
├── DELETE /{id}/                          # Delete organization
└── POST   /{id}/logo/                     # Upload organization logo
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
    "lucide-react": "^0.462.0",           // Icon library
    "clsx": "^2.1.1",                     // Conditional CSS classes
    "tailwind-merge": "^2.5.4"            // Tailwind class merging
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
npm run dev                                # Runs on http://localhost:5173
```

### **Available Scripts & Commands**
```bash
# Frontend Commands
npm run dev          # Start development server
npm run build        # Build for production  
npm run preview      # Preview production build
npm run lint         # Run ESLint

# Backend Commands
python manage.py runserver                  # Start Django server
python manage.py migrate                   # Apply database migrations
python manage.py createsuperuser           # Create admin user
python manage.py create_sample_employees    # Create sample employee data
python manage.py create_sample_admin_data   # Create sample admin data
python manage.py test                      # Run tests
python create_super_admin.py               # Create super admin
python verify_setup.py                     # Verify system setup
```

---

## 🔒 **Security & Configuration**

### **Important Configuration Files**
```
🔧 Key Config Files:
├── backend/hopesecure_backend/settings.py    # Django settings
├── vite.config.ts                            # Vite configuration
├── tailwind.config.ts                        # Tailwind CSS config
├── tsconfig.json                             # TypeScript config
└── components.json                           # shadcn/ui config
```

### **Environment Variables**
```bash
# Backend Environment (.env if needed)
DEBUG=True                                 # Development mode
SECRET_KEY=django-insecure-...             # Django secret key
DATABASE_URL=sqlite:///db.sqlite3          # Database connection
ALLOWED_HOSTS=localhost,127.0.0.1          # Allowed hosts
CORS_ALLOWED_ORIGINS=http://localhost:5173 # CORS origins (updated port)
```

---

## 📋 **Project Status & Features**

### **✅ Completed Features**
- ✅ User Authentication (Login/Logout/Registration)
- ✅ Protected Routes with Role-Based Access
- ✅ Dashboard with Real-Time Data Integration
- ✅ Template Management (CRUD Operations)
- ✅ Campaign Management with Draft/Published States
- ✅ Employee Management System
- ✅ Organization/Company Management
- ✅ Real-Time Campaign Execution Monitoring
- ✅ Department Analysis & Vulnerable Employee Tracking
- ✅ Comprehensive CRUD Operations (Edit/Delete/Create)
- ✅ Navigation Enhancements (Home/Dashboard buttons)
- ✅ REST API Backend with Complete Endpoints
- ✅ Frontend-Backend Integration
- ✅ Responsive UI Design with shadcn/ui
- ✅ Production Build Ready
- ✅ Complete Documentation Organization

### **🎯 Advanced Features Implemented**
- 🎯 **Real-Time Campaign Monitoring:** Live activity feeds and progress tracking
- 🎯 **Draft Campaign System:** Save and edit campaigns before publishing
- 🎯 **Dynamic Department Analysis:** Real-time vulnerability scoring
- 🎯 **Pre-made Template Fallbacks:** Automatic template loading when user templates unavailable
- 🎯 **Interactive Navigation:** Home and Dashboard buttons across pages
- 🎯 **Company Settings Management:** Complete organization profile management
- 🎯 **Notification System:** Campaign alerts and status updates

### **🎯 Core User Roles**
- **Super Admin:** System-wide access and management
- **Admin:** Full organizational access
- **Manager:** Campaign & employee management
- **Analyst:** Template creation & campaign execution
- **Employee:** Limited access to personal data

---

## 🚧 **Development Notes for Team**

### **Recent Major Updates (August 2025)**
1. **Navigation Enhancements:** Added Home and Dashboard buttons across all pages
2. **Real-Time Data Integration:** Replaced all hardcoded data with live data feeds
3. **CRUD Operations:** Complete Create, Read, Update, Delete functionality for campaigns
4. **Draft Management:** Full draft campaign system with edit capabilities
5. **Documentation Organization:** All .md files moved to organized "project guide" folder
6. **Department Analysis:** Real-time vulnerability tracking and employee analysis
7. **Template System:** Pre-made template fallbacks and user template management

### **Important File Interactions**
1. **Authentication Flow:** `AuthContext.tsx` ↔ `api.ts` ↔ `authentication/views.py`
2. **Routing:** `App.tsx` → `pages/*.tsx` → Protected by `ProtectedRoute.tsx`
3. **API Communication:** `hooks/useApi.ts` → `lib/api.ts` → Django REST endpoints
4. **Real-Time Features:** `useCampaigns.ts` → localStorage → Real-time UI updates
5. **Database:** Django Models → Migrations → SQLite/PostgreSQL

### **Code Organization Principles**
- **Frontend:** Component-based architecture with custom hooks for state
- **Backend:** Django apps for feature separation
- **API:** RESTful design with DRF serializers
- **Styling:** Tailwind CSS with shadcn/ui components
- **Type Safety:** TypeScript throughout frontend with proper interfaces
- **State Management:** React Context + localStorage for persistence

### **Development Best Practices**
- Always test in both dev and build modes
- Use TypeScript interfaces for API responses
- Follow Django REST framework conventions
- Maintain consistent file naming (PascalCase for components)
- Document new features and API changes
- Test CRUD operations thoroughly
- Verify real-time data flow

---

## 📞 **For Team Questions**

**Frontend Issues:** Check `src/` structure, API integration in `lib/api.ts`  
**Backend Issues:** Check Django apps in `backend/`, settings in `hopesecure_backend/settings.py`  
**Database Issues:** Check models and migrations in each app  
**Build Issues:** Check `vite.config.ts`, `package.json`, and TypeScript configs  
**Navigation Issues:** Check routing in `App.tsx` and navigation buttons in page headers  
**Real-Time Features:** Check `useCampaigns.ts` hook and localStorage integration  
**CRUD Operations:** Check individual page components for edit/delete functionality  

**Current Status:** ✅ Fully functional development and production environment with advanced features!

---

## 🎯 **Quick Start Guide**

### **For New Developers:**
1. **Clone the repository**
2. **Install dependencies:** `npm install` (frontend) + `pip install -r requirements.txt` (backend)
3. **Setup database:** `cd backend && python manage.py migrate`
4. **Create sample data:** `python manage.py create_sample_employees`
5. **Start servers:** `python manage.py runserver` (backend) + `npm run dev` (frontend)
6. **Access application:** http://localhost:5173

### **For Documentation:**
- **Main Guide:** This README.md in project guide folder
- **Backend Setup:** BACKEND_README.md
- **Integration Details:** FRONTEND_INTEGRATION.md
- **Feature Details:** Check individual .md files in project guide folder

**Happy Coding! 🚀**
