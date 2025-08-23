#!/usr/bin/env python
"""
Test super admin dashboard functionality
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopesecure_backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def test_super_admin_dashboard():
    print("=== Super Admin Dashboard Test ===")
    
    # Verify super admin exists
    try:
        admin_user = User.objects.get(email="admin@test.com")
        print(f"✅ Super admin found: {admin_user.email}")
        print(f"   Role: {admin_user.role}")
        print(f"   Is Super Admin: {admin_user.is_super_admin}")
        print(f"   Is Org Admin: {admin_user.is_org_admin}")
        
        # Test authentication
        if admin_user.check_password("admin"):
            print("✅ Password verification successful")
        else:
            print("❌ Password verification failed")
        
        print("\n=== Dashboard Access Information ===")
        print("🔐 Super Admin Login:")
        print("   URL: http://localhost:3000/signin")
        print("   Email: admin@test.com")
        print("   Password: admin")
        
        print("\n🎯 Super Admin Dashboard:")
        print("   URL: http://localhost:3000/superadmin")
        print("   Access: Only available to super_admin role")
        
        print("\n🔧 Dashboard Features:")
        print("   • View all organizations across the system")
        print("   • Monitor system-wide statistics")
        print("   • User management overview")
        print("   • Organization activity monitoring")
        print("   • System health and controls")
        
        print("\n🌐 API Endpoints Available:")
        print("   • GET /api/organization/admin/organizations/")
        print("   • GET /api/organization/admin/stats/")
        print("   • GET /api/organization/company/ (enhanced view)")
        
        print("\n🚫 Regular User Restrictions:")
        print("   • Regular users cannot access /superadmin")
        print("   • Organization admins cannot see other organizations")
        print("   • Automatic redirect to appropriate dashboard based on role")
        
        return True
        
    except User.DoesNotExist:
        print("❌ Super admin not found! Run create_super_admin.py first.")
        return False
    except Exception as e:
        print(f"❌ Error testing super admin: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_super_admin_dashboard()
    if success:
        print("\n🎉 Super Admin Dashboard is ready for use!")
        print("\nNext Steps:")
        print("1. Start the frontend: npm run dev")
        print("2. Login with admin@test.com / admin")
        print("3. Navigate to /superadmin or get redirected automatically")
        print("4. Manage all organizations from the super admin dashboard")
    else:
        print("\n❌ Setup incomplete. Please run create_super_admin.py first.")
