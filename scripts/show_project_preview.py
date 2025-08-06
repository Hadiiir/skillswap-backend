#!/usr/bin/env python
"""
Full preview of the SkillSwap Backend project
"""
import subprocess
import webbrowser
import time
import os
from pathlib import Path

def show_project_preview():
    """Display project preview"""
    print("🎬 Showing preview of SkillSwap Backend Project")
    print("=" * 50)
    
    # Check Docker status
    try:
        result = subprocess.run(['docker-compose', 'ps'], 
                              capture_output=True, text=True, check=True)
        if 'web' in result.stdout and 'Up' in result.stdout:
            print("✅ Docker containers are running")
            base_url = "http://localhost:8000"
        else:
            print("⚠️ Docker containers not running. Starting them...")
            subprocess.run(['docker-compose', 'up', '-d'], check=True)
            print("⏳ Waiting for containers to start...")
            time.sleep(10)
            base_url = "http://localhost:8000"
    except:
        print("⚠️ Docker not available. Using local development server...")
        base_url = "http://127.0.0.1:8000"
    
    # Display project info
    print("\n🚀 SkillSwap Backend - Project Info")
    print("=" * 50)
    print("📊 Project Statistics:")
    print("   • 8 Django Apps")
    print("   • 15+ Database Models") 
    print("   • 25+ API Endpoints")
    print("   • Real-time Chat System")
    print("   • Payment Integration")
    print("   • Advanced Search & Filtering")
    print("   • Multi-language Support")
    
    print("\n🔗 Important Links:")
    print(f"   • Main Website: {base_url}/")
    print(f"   • Admin Panel: {base_url}/admin/")
    print(f"   • Main API: {base_url}/api/")
    print(f"   • Skills API: {base_url}/api/skills/")
    print(f"   • Users API: {base_url}/api/auth/")
    print(f"   • Points API: {base_url}/api/points/")
    print(f"   • Chat API: {base_url}/api/chat/")
    print(f"   • Payments API: {base_url}/api/payments/")
    print(f"   • Reviews API: {base_url}/api/reviews/")
    
    print("\n🔑 Login Credentials:")
    print("   • Email: admin@skillswap.com")
    print("   • Password: admin123")
    
    print("\n📱 Available Apps:")
    print("   • accounts - User management and authentication")
    print("   • skills - Skill and service marketplace")
    print("   • points - Points and transactions system")
    print("   • chat - Real-time chat system")
    print("   • payments - Payment processing")
    print("   • reviews - Ratings and reviews system")
    print("   • notifications - Notifications system")
    
    print("\n🛠️ Advanced Features:")
    print("   • AI-Powered Recommendations")
    print("   • Advanced Search Engine")
    print("   • Real-time WebSocket Chat")
    print("   • Multi-Payment Gateway Integration")
    print("   • Advanced Security System")
    print("   • Performance Monitoring")
    print("   • Multi-language Support (EN/AR)")
    
    # Open preview in browser
    preview_file = Path(__file__).parent.parent / 'preview' / 'skillswap_backend_demo.html'
    if preview_file.exists():
        print(f"\n🌐 Opening project preview in browser...")
        webbrowser.open(f'file://{preview_file.absolute()}')
    
    # Open admin panel
    print(f"\n🔧 Opening admin panel...")
    webbrowser.open(f'{base_url}/admin/')
    
    print("\n✨ Project preview displayed successfully!")
    print("You can now explore all available features and APIs")

if __name__ == '__main__':
    show_project_preview() 
