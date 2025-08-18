# CyberGuard Backend - Django REST API

A comprehensive Django backend for the CyberGuard cybersecurity simulation platform that provides phishing simulation, employee management, and security awareness training capabilities.

## 🚀 Features

- **User Authentication & Authorization**
  - Custom user model with role-based access control
  - Token-based authentication
  - User profiles and settings

- **Template Management**
  - Phishing email templates
  - Landing page templates
  - Template categorization and tagging
  - Template preview and cloning

- **Campaign Management**
  - Create and manage phishing simulation campaigns
  - Target employee selection
  - Real-time campaign monitoring
  - Event tracking and analytics

- **Employee Management**
  - Employee profiles and departments
  - Risk assessment and scoring
  - Training records and compliance

- **Reports & Analytics**
  - Campaign performance reports
  - Security metrics and KPIs
  - Dashboard widgets and visualizations

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd statuscode-backup/backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install django djangorestframework django-cors-headers pillow
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Load Sample Data

```bash
python manage.py populate_sample_data
```

### 8. Start Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 🔗 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | User registration |
| POST | `/api/auth/login/` | User login |
| POST | `/api/auth/logout/` | User logout |
| GET | `/api/auth/profile/` | Get user profile |
| PUT | `/api/auth/profile/update/` | Update user profile |
| POST | `/api/auth/password/change/` | Change password |
| GET | `/api/auth/dashboard/stats/` | Dashboard statistics |

### Template Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/templates/` | List all templates |
| POST | `/api/templates/` | Create new template |
| GET | `/api/templates/{id}/` | Get template details |
| PUT | `/api/templates/{id}/` | Update template |
| DELETE | `/api/templates/{id}/` | Delete template |
| POST | `/api/templates/{id}/clone/` | Clone template |
| GET | `/api/templates/{id}/preview/` | Preview template |
| GET | `/api/templates/stats/` | Template statistics |
| GET | `/api/templates/categories/` | Template categories |
| GET | `/api/templates/by-category/` | Templates by category |
| GET | `/api/templates/tags/` | Template tags |

### Campaign Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/campaigns/` | List all campaigns |
| POST | `/api/campaigns/` | Create new campaign |
| GET | `/api/campaigns/{id}/` | Get campaign details |
| PUT | `/api/campaigns/{id}/` | Update campaign |
| DELETE | `/api/campaigns/{id}/` | Delete campaign |
| GET | `/api/campaigns/stats/` | Campaign statistics |

### Employee Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/employees/` | List all employees |
| POST | `/api/employees/` | Create new employee |
| GET | `/api/employees/{id}/` | Get employee details |
| PUT | `/api/employees/{id}/` | Update employee |
| DELETE | `/api/employees/{id}/` | Delete employee |
| GET | `/api/employees/departments/` | List departments |
| POST | `/api/employees/departments/` | Create department |
| GET | `/api/employees/stats/` | Employee statistics |

### Report Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reports/` | List all reports |
| POST | `/api/reports/` | Create new report |
| GET | `/api/reports/{id}/` | Get report details |
| PUT | `/api/reports/{id}/` | Update report |
| DELETE | `/api/reports/{id}/` | Delete report |

## 🔐 Authentication

The API uses token-based authentication. Include the token in the Authorization header:

```
Authorization: Token your_token_here
```

### Login Example

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@cyberguard.com",
    "password": "your_password"
  }'
```

Response:
```json
{
  "user": {
    "id": 1,
    "email": "admin@cyberguard.com",
    "username": "admin",
    "first_name": "Admin",
    "last_name": "User",
    "role": "admin"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "message": "Login successful"
}
```

## 📊 Database Schema

### Key Models

- **User**: Extended Django user model with roles and departments
- **Template**: Phishing email and landing page templates
- **Campaign**: Phishing simulation campaigns
- **CampaignTarget**: Individual targets within campaigns
- **Employee**: Employee profiles for targeting
- **Department**: Organizational departments
- **Report**: Generated reports and analytics

### User Roles

- `admin`: Full system access
- `manager`: Can manage campaigns and view reports
- `analyst`: Can create templates and run campaigns
- `employee`: Limited access to personal data

## 🛡️ Security Features

- CORS protection for frontend integration
- Token-based authentication
- Role-based access control
- Input validation and sanitization
- SQL injection protection
- XSS protection

## 📁 Project Structure

```
backend/
├── cyberguard_backend/     # Main project settings
├── authentication/        # User authentication app
├── templates/             # Template management app
├── campaigns/             # Campaign management app
├── employees/             # Employee management app
├── reports/               # Reports and analytics app
├── media/                 # Uploaded files
├── db.sqlite3            # SQLite database
└── manage.py             # Django management script
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```
DEBUG=True
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Database Configuration

The project uses SQLite by default. For production, consider PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cyberguard_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

## 📈 Sample Data

The backend includes sample data for testing:

- Sample users with different roles
- Template examples for various phishing scenarios
- Sample campaigns with targets and events
- Department and employee data

## 🚀 Deployment

For production deployment:

1. Set `DEBUG=False` in settings
2. Configure production database
3. Set up static file serving
4. Use a production WSGI server (gunicorn)
5. Configure HTTPS
6. Set up monitoring and logging

## 🤝 Frontend Integration

This backend is designed to work with the React frontend. Make sure to:

1. Update CORS settings for your frontend domain
2. Configure the frontend API base URL to point to this backend
3. Handle authentication tokens in frontend requests

## 📚 API Documentation

Detailed API documentation with request/response examples is available through:

- Django REST Framework browsable API at `/api/`
- Swagger/OpenAPI documentation (can be added with drf-spectacular)

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure frontend URL is in `CORS_ALLOWED_ORIGINS`
2. **Authentication Errors**: Check token format in Authorization header
3. **Migration Errors**: Run `python manage.py makemigrations` before `migrate`
4. **Permission Errors**: Verify user roles and permissions

### Debug Mode

Enable debug mode for development:

```python
DEBUG = True
```

This will show detailed error messages and enable the Django debug toolbar.

## 📞 Support

For issues and questions:

1. Check the Django documentation
2. Review the DRF documentation
3. Check existing GitHub issues
4. Create a new issue with detailed information

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
