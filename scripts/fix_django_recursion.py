#!/usr/bin/env python3
"""
Fix Django recursion error in gettext_lazy
"""
import os
import sys
import subprocess
import shutil

def fix_django_recursion():
    """Fix Django recursion error"""
    print("🔧 Fixing Django recursion error...")
    
    # 1. Remove problematic virtual environment
    venv_path = "venv"
    if os.path.exists(venv_path):
        print(f"Removing existing virtual environment: {venv_path}")
        shutil.rmtree(venv_path)
    
    # 2. Create fresh virtual environment
    print("Creating fresh virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    
    # 3. Activate and install requirements
    if os.name == 'nt':  # Windows
        pip_path = os.path.join("venv", "Scripts", "pip")
        python_path = os.path.join("venv", "Scripts", "python")
    else:  # Unix/Linux
        pip_path = os.path.join("venv", "bin", "pip")
        python_path = os.path.join("venv", "bin", "python")
    
    print("Upgrading pip...")
    subprocess.run([python_path, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    
    print("Installing requirements...")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
    
    # 4. Test Django installation
    print("Testing Django installation...")
    try:
        subprocess.run([python_path, "-c", "import django; print(f'Django {django.get_version()} installed successfully')"], check=True)
        print("✅ Django installation fixed!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Django installation still has issues")
        return False

if __name__ == "__main__":
    fix_django_recursion()
