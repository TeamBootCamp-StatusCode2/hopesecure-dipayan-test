#!/usr/bin/env python
"""
PostgreSQL Database Setup Script for HopeSecure
This script creates the PostgreSQL database and migrates data from SQLite
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2 import sql
import django
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent
sys.path.append(str(backend_dir))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

def create_postgresql_database():
    """Create PostgreSQL database if it doesn't exist"""
    try:
        # Connection parameters
        db_params = {
            'host': 'localhost',
            'port': '5432',
            'user': 'postgres',
            'password': 'speed123'
        }
        
        # Connect to PostgreSQL server (not to specific database)
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
            ('hopesecure-statuscode',)
        )
        
        if cursor.fetchone():
            print("✅ Database 'hopesecure-statuscode' already exists")
        else:
            # Create database
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier('hopesecure-statuscode')
                )
            )
            print("✅ Database 'hopesecure-statuscode' created successfully")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ PostgreSQL Error: {e}")
        print("Make sure PostgreSQL is running and credentials are correct")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def setup_postgresql():
    """Complete PostgreSQL setup process"""
    print("🐘 Setting up PostgreSQL for HopeSecure...")
    
    # Step 1: Create database
    if not create_postgresql_database():
        return False
    
    # Step 2: Set environment variable for this session
    os.environ['USE_POSTGRES'] = 'True'
    
    # Step 3: Run migrations
    print("🔄 Running Django migrations...")
    try:
        subprocess.run([
            sys.executable, 'manage.py', 'migrate'
        ], check=True, cwd=backend_dir)
        print("✅ Migrations completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        return False
    
    # Step 4: Create sample data
    print("📊 Creating sample data...")
    try:
        subprocess.run([
            sys.executable, 'manage.py', 'create_sample_employees'
        ], check=True, cwd=backend_dir)
        print("✅ Sample employees created")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Sample employee creation failed (this is optional): {e}")
    
    print("\n🎉 PostgreSQL setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Make sure your .env file has USE_POSTGRES=True")
    print("2. Run: python manage.py runserver")
    print("3. Your team members can keep using SQLite by setting USE_POSTGRES=False")
    
    return True

if __name__ == '__main__':
    setup_postgresql()
