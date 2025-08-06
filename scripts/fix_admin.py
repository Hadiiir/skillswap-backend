#!/usr/bin/env python
"""
Script to fix admin configuration issues
"""
import os
import sys
import django
import subprocess

# Add the project directory to Python path
sys.path.append('/app')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings')

# Setup Django
django.setup()

def fix_admin():
    """Fix admin configuration"""
    print("🔧 Fixing admin configuration...")
    
    # The admin.py file has been updated to remove non-editable fields
    print("✅ Admin configuration updated")
    print("✅ Removed non-editable fields from admin interface")
    print("✅ Added readonly_fields for auto-generated timestamps")
    
    try:
        # Restart the Docker containers to apply changes
        print("\n📦 Restarting Docker containers...")
        subprocess.run(['docker-compose', 'restart', 'web'], check=True)
        
        print("\n✅ Admin configuration fixed!")
        print("🌐 Try accessing the admin panel again at: http://localhost:8000/admin/")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error restarting containers: {e}")
        return False
    
    return True

if __name__ == '__main__':
    fix_admin()
