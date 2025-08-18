# CyberGuard - Complete Cybersecurity Simulation Platform

A full-stack cybersecurity awareness platform combining a React frontend with a Django REST API backend.

## 🏗️ Project Structure

```
statuscode-backup/
├── 📁 frontend/                 # React + TypeScript + Vite
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/             # Application pages
│   │   ├── data/              # Static data (to be replaced with API)
│   │   ├── hooks/             # Custom React hooks
│   │   └── lib/               # Utilities and configurations
│   ├── public/                # Static assets
│   └── package.json           # Frontend dependencies
│
├── 📁 backend/                  # Django REST API
│   ├── cyberguard_backend/    # Main Django project
│   ├── authentication/       # User management
│   ├── templates/            # Phishing templates
│   ├── campaigns/            # Campaign management
│   ├── employees/            # Employee management
│   ├── reports/              # Analytics and reports
│   ├── media/                # File uploads
│   ├── db.sqlite3           # SQLite database
│   └── requirements.txt      # Backend dependencies
│
└── README.md                 # This file
```

## 🚀 Quick Start Guide

### Prerequisites
- Node.js 16+ (for frontend)
- Python 3.8+ (for backend)
- Git

### 1. Backend Setup (Django API)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data
python manage.py populate_sample_data

# Start Django server
python manage.py runserver
```

Backend will be available at: `http://127.0.0.1:8000/`

### 2. Frontend Setup (React)

```bash
# Navigate to frontend directory (in new terminal)
cd ../

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:5173/`

## 🔗 Integration Status

### Current State
- ✅ **Frontend**: Fully functional React app with mock data
- ✅ **Backend**: Complete Django REST API with all endpoints
- ⏳ **Integration**: Ready for connection (requires API client setup)

### What's Working

#### Frontend (React)
- Complete cybersecurity simulation UI
- Dashboard with campaign metrics
- Template management system
- Campaign creation and monitoring
- Employee management interface
- Authentication pages (sign in/up)
- Responsive design with Tailwind CSS

#### Backend (Django)
- RESTful API with authentication
- User management with roles
- Template CRUD operations
- Campaign management system
- Employee tracking
- Real-time event logging
- Sample data for testing

## 🔧 API Endpoints

The Django backend provides these key endpoints:

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile

### Templates
- `GET /api/templates/` - List templates
- `POST /api/templates/` - Create template
- `GET /api/templates/{id}/` - Get template details
- `PUT /api/templates/{id}/` - Update template

### Campaigns
- `GET /api/campaigns/` - List campaigns
- `POST /api/campaigns/` - Create campaign
- `GET /api/campaigns/{id}/` - Get campaign details
- `PUT /api/campaigns/{id}/` - Update campaign

### Employees
- `GET /api/employees/` - List employees
- `POST /api/employees/` - Create employee
- `GET /api/employees/{id}/` - Get employee details

## 🔐 Authentication

The system uses token-based authentication:

1. **Login**: Get token with credentials
2. **Requests**: Include `Authorization: Token <token>` header
3. **Logout**: Invalidate token

### Sample Accounts
```
Admin: admin@cyberguard.com / [your-password]
Manager: manager@cyberguard.com / password123
Analyst: analyst@cyberguard.com / password123
```

## 📊 Features

### 🎯 Phishing Simulation
- Create phishing email templates
- Design landing pages
- Configure campaign parameters
- Target specific employees/groups

### 👥 Employee Management
- Import employee data
- Department organization
- Risk level assessment
- Training records tracking

### 📈 Analytics & Reporting
- Real-time campaign monitoring
- Success rate calculations
- Employee vulnerability scoring
- Department-wise analytics

### 🛡️ Security Features
- Role-based access control
- Secure token authentication
- CORS protection
- Input validation

## 🔄 Integration Steps

To connect the frontend with the backend:

1. **Setup API Client** - Create HTTP client with authentication
2. **Update Authentication** - Replace mock login with real API calls
3. **Connect Dashboard** - Fetch real campaign and employee data
4. **Template Integration** - Use API for template CRUD operations
5. **Campaign Management** - Connect campaign creation and monitoring
6. **Real-time Updates** - Implement polling or WebSockets

See `backend/FRONTEND_INTEGRATION.md` for detailed integration guide.

## 🧪 Testing

### Backend Testing
```bash
cd backend
python manage.py test
```

### Frontend Testing
```bash
npm run test
```

### API Testing
```bash
cd backend
python test_api.py
```

## 🌐 Deployment

### Development
- Frontend: Vite dev server on port 5173
- Backend: Django dev server on port 8000

### Production
- Frontend: Build with `npm run build` and serve static files
- Backend: Use production WSGI server (gunicorn)
- Database: PostgreSQL recommended for production
- Hosting: AWS, DigitalOcean, or similar

## 📚 Documentation

- `backend/README.md` - Backend setup and API documentation
- `backend/FRONTEND_INTEGRATION.md` - Integration guide
- `README.md` (this file) - Project overview

## 🔧 Technology Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Radix UI** - Component library
- **React Router** - Navigation
- **Lucide React** - Icons

### Backend
- **Django 5.2** - Web framework
- **Django REST Framework** - API framework
- **SQLite** - Database (development)
- **Pillow** - Image processing
- **django-cors-headers** - CORS handling

## 🚨 Security Considerations

### Development
- CORS enabled for localhost
- Debug mode enabled
- Secret key in settings (change for production)
- SQLite database (migrate to PostgreSQL for production)

### Production
- Disable debug mode
- Use environment variables for secrets
- Configure HTTPS
- Set up proper CORS origins
- Use production database
- Implement rate limiting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- Check documentation in `backend/` and frontend `src/` directories
- Review API endpoints with Django REST Framework browsable API
- Create issues for bugs or feature requests

## 🎯 Next Steps

1. **Complete Integration** - Connect frontend to backend API
2. **Add Real-time Features** - WebSocket support for live updates
3. **Enhanced Security** - Two-factor authentication, audit logs
4. **Advanced Analytics** - More detailed reporting and insights
5. **Mobile Support** - React Native app or PWA features
6. **Email Integration** - Real email sending capabilities
7. **Advanced Templates** - Rich text editor, template marketplace

Your cybersecurity simulation platform is ready for integration and deployment! 🚀
