# 🔒 Production Security Checklist

## ⚠️ CRITICAL - Change Before Production:

### 1. Secret Key
```python
# ❌ NEVER use this in production:
SECRET_KEY = 'django-insecure-8qf634_3urs411_&t8)c0jr31_^ly5-@#y9)dj3_li*!75o6^n'

# ✅ Use environment variable:
SECRET_KEY = os.getenv('SECRET_KEY')
```

### 2. Debug Mode
```python
# ❌ NEVER set DEBUG=True in production
DEBUG = False
```

### 3. Database Security
```python
# ❌ Remove hardcoded passwords
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),  # Use strong password
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

### 4. CORS Configuration
```python
# ❌ Remove CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

### 5. ALLOWED_HOSTS
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

## 🛡️ Additional Security Settings:

### SSL/HTTPS
```python
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Session Security
```python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### Password Validation
```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

## 📝 Environment Variables (.env):
```
SECRET_KEY=your_very_long_random_secret_key_here
DEBUG=False
DB_NAME=your_production_db_name
DB_USER=your_db_user
DB_PASSWORD=your_secure_db_password
DB_HOST=your_db_host
DB_PORT=5432
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 🚀 Deployment Checklist:
- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure production database
- [ ] Set up HTTPS
- [ ] Configure proper CORS origins
- [ ] Set ALLOWED_HOSTS
- [ ] Use environment variables for all secrets
- [ ] Set up proper logging
- [ ] Configure static file serving
- [ ] Set up monitoring
- [ ] Regular security updates
