# 🐘 Database Configuration Guide - HopeSecure

## 📋 **How Database Selection Works**

This project supports both **PostgreSQL** and **SQLite** databases through environment-based configuration.

## 🔧 **For Team Members (SQLite - Easy Setup)**

### **Option 1: Use SQLite (Recommended for quick development)**

1. **Make sure `.env` file has:**
   ```env
   USE_POSTGRES=False
   ```
   **OR** comment out the line:
   ```env
   # USE_POSTGRES=True
   ```

2. **Run the project:**
   ```bash
   cd backend
   python manage.py migrate
   python manage.py create_sample_employees
   python manage.py runserver
   ```

3. **That's it! ✅** SQLite database will be created automatically.

---

## 🐘 **For Production/Advanced Users (PostgreSQL)**

### **Option 2: Use PostgreSQL (Better for production)**

1. **Install PostgreSQL:**
   - Download from: https://www.postgresql.org/download/
   - Install with username: `postgres` and password: `speed123`

2. **Set environment in `.env` file:**
   ```env
   USE_POSTGRES=True
   DB_NAME=hopesecure-statuscode
   DB_USER=postgres
   DB_PASSWORD=speed123
   DB_HOST=localhost
   DB_PORT=5432
   ```

3. **Run setup:**
   ```bash
   cd backend
   python setup_postgresql.py
   python manage.py runserver
   ```

---

## 🤝 **Team Collaboration**

### **Perfect for Mixed Teams:**
- **Team Lead:** Can use PostgreSQL for production-like environment
- **Developers:** Can use SQLite for quick local development
- **Same codebase, different databases** - no conflicts!

### **Switching Between Databases:**
```bash
# Use PostgreSQL
echo "USE_POSTGRES=True" > backend/.env

# Use SQLite  
echo "USE_POSTGRES=False" > backend/.env
```

---

## 🔍 **Current Database Status**

You can check which database is being used:
```bash
cd backend
python manage.py dbshell --help
```

The console will show:
- 🐘 **"Using PostgreSQL Database"** - if PostgreSQL is active
- 🗃️ **"Using SQLite Database"** - if SQLite is active

---

## 📊 **Database Files Location**

### **SQLite:**
- File: `backend/db.sqlite3`
- Portable and included in project

### **PostgreSQL:**
- Server: localhost:5432
- Database: `hopesecure-statuscode`
- Not included in project (server-based)

---

## 🚀 **Quick Commands**

```bash
# Check current database
cd backend && python manage.py dbshell --help

# Migrate database  
python manage.py migrate

# Create sample data
python manage.py create_sample_employees

# Reset database (SQLite only)
rm db.sqlite3 && python manage.py migrate

# Setup PostgreSQL (if needed)
python setup_postgresql.py
```

---

## 📞 **Need Help?**

1. **SQLite Issues:** Usually auto-resolved by running `python manage.py migrate`
2. **PostgreSQL Issues:** Check if PostgreSQL service is running
3. **Environment Issues:** Verify `.env` file configuration

**Both databases work perfectly with the same codebase! 🎯**
