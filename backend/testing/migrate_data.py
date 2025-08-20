#!/usr/bin/env python
"""
Data Migration Script: SQLite to PostgreSQL
This script migrates user data from SQLite to PostgreSQL database
"""

import os
import sys
import sqlite3
import django
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent
sys.path.append(str(backend_dir))

def migrate_sqlite_to_postgresql():
    """Migrate user data from SQLite to PostgreSQL"""
    
    print("🔄 Starting data migration from SQLite to PostgreSQL...")
    
    # Step 1: Check if SQLite database exists
    sqlite_db_path = backend_dir / 'db.sqlite3'
    if not sqlite_db_path.exists():
        print("❌ SQLite database not found. Nothing to migrate.")
        return False
    
    # Step 2: Connect to SQLite database
    try:
        sqlite_conn = sqlite3.connect(sqlite_db_path)
        sqlite_cursor = sqlite_conn.cursor()
        print("✅ Connected to SQLite database")
    except Exception as e:
        print(f"❌ Failed to connect to SQLite: {e}")
        return False
    
    # Step 3: Setup Django with PostgreSQL
    os.environ['USE_POSTGRES'] = 'True'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
    django.setup()
    
    from authentication.models import User
    from django.contrib.auth.hashers import make_password
    
    print("✅ Connected to PostgreSQL database")
    
    # Step 4: Fetch users from SQLite
    try:
        sqlite_cursor.execute("""
            SELECT id, email, username, first_name, last_name, password, 
                   is_staff, is_active, is_superuser, date_joined
            FROM authentication_user
        """)
        sqlite_users = sqlite_cursor.fetchall()
        print(f"📊 Found {len(sqlite_users)} users in SQLite")
    except Exception as e:
        print(f"❌ Failed to fetch users from SQLite: {e}")
        return False
    
    # Step 5: Migrate users to PostgreSQL
    migrated_count = 0
    skipped_count = 0
    
    for user_data in sqlite_users:
        (user_id, email, username, first_name, last_name, 
         password, is_staff, is_active, is_superuser, date_joined) = user_data
        
        try:
            # Check if user already exists in PostgreSQL
            if User.objects.filter(email=email).exists():
                print(f"⚠️  User {email} already exists, skipping...")
                skipped_count += 1
                continue
            
            # Create user in PostgreSQL
            user = User.objects.create(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,  # Password is already hashed
                is_staff=is_staff,
                is_active=is_active,
                is_superuser=is_superuser,
            )
            
            print(f"✅ Migrated user: {email}")
            migrated_count += 1
            
        except Exception as e:
            print(f"❌ Failed to migrate user {email}: {e}")
            continue
    
    # Step 6: Close SQLite connection
    sqlite_conn.close()
    
    # Step 7: Summary
    print(f"\n🎉 Migration completed!")
    print(f"✅ Migrated: {migrated_count} users")
    print(f"⚠️  Skipped: {skipped_count} users")
    print(f"📊 Total PostgreSQL users: {User.objects.count()}")
    
    # Step 8: Show all users
    print(f"\n👥 Current users in PostgreSQL:")
    for user in User.objects.all():
        print(f"   📧 {user.email} ({user.username})")
    
    return True

if __name__ == '__main__':
    migrate_sqlite_to_postgresql()
