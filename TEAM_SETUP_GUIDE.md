# 🚀 HopeSecure - Team Setup Guide

## 🎯 **Quick Start for New Team Members**

### **Method 1: Automated Setup (Recommended)**
```bash
# 1. Clone the repository
git clone <repository-url>
cd hopesecure-dipayan-test/backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run setup script
python setup_env.py

# 4. Follow the prompts to choose database
# 5. Run the application
python manage.py migrate
python manage.py create_sample_employees
python manage.py runserver
```

### **Method 2: Manual Setup**
```bash
# 1. Create environment file
cp .env.example .env

# 2. Edit .env file with your settings
# For SQLite (easy): USE_POSTGRES=False
# For PostgreSQL: USE_POSTGRES=True + database credentials

# 3. Run the application
python manage.py migrate
python manage.py create_sample_employees
python manage.py runserver
```

## 🛢️ **Database Options**

### **Option A: SQLite (Recommended for beginners)**
- ✅ No additional setup required
- ✅ Perfect for development
- ✅ Automatic database creation
- ✅ Set `USE_POSTGRES=False` in .env

### **Option B: PostgreSQL (For production-like environment)**
- 🐘 Install PostgreSQL locally
- 🔧 Create database: `hopesecure-statuscode`
- ⚙️ Set `USE_POSTGRES=True` in .env
- 📝 Configure database credentials

## 🔒 **Security Notes**

### **Important: .env File**
- ❌ **NEVER commit .env to git**
- ✅ Always use .env.example as template
- 🔐 Each team member creates their own .env
- 🚫 .env is already in .gitignore

### **Environment Variables**
```env
# Example .env file structure
USE_POSTGRES=False              # or True for PostgreSQL
SECRET_KEY=your-unique-secret
DB_NAME=hopesecure-statuscode   # only for PostgreSQL
DB_USER=postgres                # only for PostgreSQL
DB_PASSWORD=your-password       # only for PostgreSQL
```

## 👥 **Team Collaboration**

### **For Different Database Preferences:**
- **Team Lead:** Uses PostgreSQL (`USE_POSTGRES=True`)
- **Developers:** Use SQLite (`USE_POSTGRES=False`) 
- **Same codebase, different databases**
- **No configuration conflicts**

### **Sharing Changes:**
```bash
# When sharing code changes:
git add .
git commit -m "Your changes"
git push

# Note: .env file is NOT included in commits
# Each team member manages their own .env
```

## 🆘 **Troubleshooting**

### **Environment Issues:**
```bash
# Reset environment
rm .env
python setup_env.py

# Check current configuration
python -c "import os; print('Database:', 'PostgreSQL' if os.getenv('USE_POSTGRES')=='True' else 'SQLite')"
```

### **Database Issues:**
```bash
# SQLite reset
rm db.sqlite3
python manage.py migrate

# PostgreSQL reset
python manage.py migrate
```

### **Common Problems:**
1. **"Settings not configured"** → Run `python setup_env.py`
2. **"Database connection failed"** → Check PostgreSQL service/credentials
3. **"Module not found"** → Run `pip install -r requirements.txt`

## 📞 **Need Help?**

1. **Quick Setup:** Run `python setup_env.py`
2. **Database Guide:** See `DATABASE_GUIDE.md`
3. **Environment Issues:** Check `.env.example` for reference

**Happy Coding! 🎉**
