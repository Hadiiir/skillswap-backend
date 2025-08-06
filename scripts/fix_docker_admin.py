#!/usr/bin/env python
"""
Fix Docker admin configuration and create superuser
"""
import subprocess
import sys

def fix_docker_admin():
    """Fix admin configuration in Docker environment"""
    print("🔧 Fixing SkillSwap Docker Admin Configuration")
    print("=" * 50)
    
    try:
        # Restart web container to apply admin fixes
        print("🔄 Restarting web container...")
        subprocess.run(['docker-compose', 'restart', 'web'], check=True)
        
        # Wait a moment for container to start
        import time
        time.sleep(3)
        
        # Run migrations
        print("📦 Running migrations...")
        subprocess.run([
            'docker-compose', 'exec', '-T', 'web',
            'python', 'manage.py', 'migrate'
        ], check=True)
        
        # Create superuser
        print("👤 Creating superuser...")
        create_superuser_script = '''
from accounts.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        email="admin@skillswap.com",
        password="admin123",
        first_name="Admin",
        last_name="User"
    )
    print("✅ Superuser created successfully!")
else:
    print("ℹ️ Superuser already exists!")
'''
        
        subprocess.run([
            'docker-compose', 'exec', '-T', 'web',
            'python', 'manage.py', 'shell', '-c', create_superuser_script
        ], check=True)
        
        # Load sample data
        print("📊 Loading sample data...")
        subprocess.run([
            'docker-compose', 'exec', '-T', 'web',
            'python', 'create_sample_data.py'
        ], check=True)
        
        print("\n✅ Docker admin configuration fixed!")
        print("🌐 Access your application:")
        print("   Main site: http://localhost:8000/")
        print("   Admin panel: http://localhost:8000/admin/")
        print("   API endpoints: http://localhost:8000/api/")
        print("")
        print("🔑 Admin credentials:")
        print("   Email: admin@skillswap.com")
        print("   Password: admin123")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error fixing Docker admin: {e}")
        return False
    
    return True

if __name__ == '__main__':
    fix_docker_admin()
