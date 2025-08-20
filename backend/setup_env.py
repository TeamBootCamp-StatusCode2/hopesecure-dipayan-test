#!/usr/bin/env python3
"""
Environment Setup Script for HopeSecure
This script helps new team members set up their environment easily
"""

import os
import shutil
import sys
from pathlib import Path

def setup_environment():
    """Setup environment for new team members"""
    backend_dir = Path(__file__).parent
    env_file = backend_dir / '.env'
    env_example = backend_dir / '.env.example'
    
    print("🚀 HopeSecure Environment Setup")
    print("=" * 40)
    
    # Check if .env already exists
    if env_file.exists():
        print("✅ .env file already exists")
        choice = input("Do you want to recreate it? (y/N): ").lower()
        if choice != 'y':
            print("⏭️  Skipping .env creation")
            return check_current_config()
    
    # Copy .env.example to .env
    if env_example.exists():
        shutil.copy2(env_example, env_file)
        print("✅ Created .env file from .env.example")
    else:
        print("❌ .env.example not found!")
        return False
    
    # Ask user preference
    print("\n🔧 Database Setup Options:")
    print("1. SQLite (Easy, no extra setup needed)")
    print("2. PostgreSQL (Advanced, better for production)")
    
    choice = input("\nChoose your database (1/2) [1]: ").strip()
    
    if choice == '2':
        setup_postgresql_env()
    else:
        setup_sqlite_env()
    
    print("\n✅ Environment setup completed!")
    print("\n📋 Next steps:")
    print("1. pip install -r requirements.txt")
    print("2. python manage.py migrate")
    print("3. python manage.py create_sample_employees")
    print("4. python manage.py runserver")
    
    return True

def setup_sqlite_env():
    """Configure for SQLite"""
    print("\n🗃️  Configuring for SQLite...")
    
    env_content = []
    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('USE_POSTGRES='):
                env_content.append('USE_POSTGRES=False\n')
            elif line.startswith('SECRET_KEY=your-secret-key-here'):
                # Generate a simple secret key for development
                import secrets
                secret_key = 'django-insecure-' + secrets.token_urlsafe(40)
                env_content.append(f'SECRET_KEY={secret_key}\n')
            else:
                env_content.append(line)
    
    with open('.env', 'w') as f:
        f.writelines(env_content)
    
    print("✅ SQLite configuration complete")

def setup_postgresql_env():
    """Configure for PostgreSQL"""
    print("\n🐘 Configuring for PostgreSQL...")
    
    # Get PostgreSQL credentials
    db_name = input("Database name [hopesecure-statuscode]: ").strip() or "hopesecure-statuscode"
    db_user = input("PostgreSQL username [postgres]: ").strip() or "postgres"
    db_password = input("PostgreSQL password: ").strip()
    
    if not db_password:
        print("❌ Password is required for PostgreSQL")
        return setup_sqlite_env()
    
    env_content = []
    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('USE_POSTGRES='):
                env_content.append('USE_POSTGRES=True\n')
            elif line.startswith('DB_NAME='):
                env_content.append(f'DB_NAME={db_name}\n')
            elif line.startswith('DB_USER='):
                env_content.append(f'DB_USER={db_user}\n')
            elif line.startswith('DB_PASSWORD='):
                env_content.append(f'DB_PASSWORD={db_password}\n')
            elif line.startswith('SECRET_KEY=your-secret-key-here'):
                import secrets
                secret_key = 'django-insecure-' + secrets.token_urlsafe(40)
                env_content.append(f'SECRET_KEY={secret_key}\n')
            else:
                env_content.append(line)
    
    with open('.env', 'w') as f:
        f.writelines(env_content)
    
    print("✅ PostgreSQL configuration complete")
    print("⚠️  Make sure PostgreSQL is installed and running!")

def check_current_config():
    """Check current configuration"""
    try:
        with open('.env', 'r') as f:
            content = f.read()
            if 'USE_POSTGRES=True' in content:
                print("📊 Current setup: PostgreSQL")
            else:
                print("📊 Current setup: SQLite")
        return True
    except FileNotFoundError:
        print("❌ .env file not found")
        return False

if __name__ == '__main__':
    if not setup_environment():
        sys.exit(1)
