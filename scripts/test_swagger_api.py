#!/usr/bin/env python3
"""
Comprehensive API testing script for SkillSwap using Swagger documentation
"""

import requests
import json
import sys
from datetime import datetime

class SkillSwapAPITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.access_token = None
        self.session = requests.Session()
        
    def print_status(self, message, status="info"):
        colors = {
            "info": "\033[0;34m",      # Blue
            "success": "\033[0;32m",   # Green
            "warning": "\033[1;33m",   # Yellow
            "error": "\033[0;31m",     # Red
            "reset": "\033[0m"         # Reset
        }
        
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        print(f"{colors.get(status, '')}{icons.get(status, '')} {message}{colors['reset']}")
    
    def test_swagger_endpoints(self):
        """Test Swagger documentation endpoints"""
        self.print_status("Testing Swagger Documentation Endpoints", "info")
        
        endpoints = {
            "Root API": "/",
            "Swagger UI": "/swagger/",
            "ReDoc": "/redoc/",
            "Swagger JSON": "/swagger.json"
        }
        
        for name, endpoint in endpoints.items():
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                if response.status_code == 200:
                    self.print_status(f"{name}: Available at {self.base_url}{endpoint}", "success")
                else:
                    self.print_status(f"{name}: Failed (HTTP {response.status_code})", "error")
            except Exception as e:
                self.print_status(f"{name}: Error - {str(e)}", "error")
    
    def register_test_user(self):
        """Register a test user"""
        self.print_status("Registering test user", "info")
        
        user_data = {
            "email": f"testuser_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "first_name": "Test",
            "last_name": "User"
        }
        
        try:
            response = self.session.post(f"{self.api_url}/auth/register/", json=user_data)
            if response.status_code == 201:
                self.print_status("User registered successfully", "success")
                return user_data
            else:
                self.print_status(f"Registration failed: {response.text}", "error")
                return None
        except Exception as e:
            self.print_status(f"Registration error: {str(e)}", "error")
            return None
    
    def login_user(self, email, password):
        """Login user and get access token"""
        self.print_status("Logging in user", "info")
        
        login_data = {
            "email": email,
            "password": password
        }
        
        try:
            response = self.session.post(f"{self.api_url}/auth/login/", json=login_data)
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('tokens', {}).get('access')
                if self.access_token:
                    self.session.headers.update({
                        'Authorization': f'Bearer {self.access_token}'
                    })
                    self.print_status("Login successful", "success")
                    return True
                else:
                    self.print_status("No access token received", "error")
                    return False
            else:
                self.print_status(f"Login failed: {response.text}", "error")
                return False
        except Exception as e:
            self.print_status(f"Login error: {str(e)}", "error")
            return False
    
    def test_protected_endpoints(self):
        """Test protected API endpoints"""
        self.print_status("Testing Protected API Endpoints", "info")
        
        endpoints = [
            ("GET", "/auth/profile/", "User Profile"),
            ("GET", "/skills/", "Skills List"),
            ("GET", "/points/balance/", "Points Balance"),
            ("GET", "/chat/conversations/", "Chat Conversations"),
            ("GET", "/payments/transactions/", "Payment Transactions"),
            ("GET", "/reviews/", "Reviews"),
            ("GET", "/notifications/", "Notifications"),
        ]
        
        for method, endpoint, name in endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{self.api_url}{endpoint}")
                elif method == "POST":
                    response = self.session.post(f"{self.api_url}{endpoint}")
                
                if response.status_code in [200, 201]:
                    self.print_status(f"{name}: Working (HTTP {response.status_code})", "success")
                elif response.status_code == 401:
                    self.print_status(f"{name}: Requires authentication (HTTP 401)", "warning")
                else:
                    self.print_status(f"{name}: Failed (HTTP {response.status_code})", "error")
                    
            except Exception as e:
                self.print_status(f"{name}: Error - {str(e)}", "error")
    
    def test_public_endpoints(self):
        """Test public API endpoints"""
        self.print_status("Testing Public API Endpoints", "info")
        
        endpoints = [
            ("GET", "/skills/categories/", "Skill Categories"),
            ("GET", "/points/packages/", "Points Packages"),
        ]
        
        for method, endpoint, name in endpoints:
            try:
                response = self.session.get(f"{self.api_url}{endpoint}")
                if response.status_code == 200:
                    self.print_status(f"{name}: Working", "success")
                    # Show sample data
                    try:
                        data = response.json()
                        if isinstance(data, dict) and 'results' in data:
                            count = len(data['results'])
                            self.print_status(f"  └─ Found {count} items", "info")
                        elif isinstance(data, list):
                            self.print_status(f"  └─ Found {len(data)} items", "info")
                    except:
                        pass
                else:
                    self.print_status(f"{name}: Failed (HTTP {response.status_code})", "error")
                    
            except Exception as e:
                self.print_status(f"{name}: Error - {str(e)}", "error")
    
    def create_test_skill(self):
        """Create a test skill"""
        if not self.access_token:
            self.print_status("Cannot create skill - not authenticated", "warning")
            return
            
        self.print_status("Creating test skill", "info")
        
        skill_data = {
            "category": 1,
            "title": "Python Programming Test",
            "title_ar": "اختبار برمجة Python",
            "description": "I will teach you Python programming basics",
            "description_ar": "سأعلمك أساسيات برمجة Python",
            "points_required": 100,
            "estimated_duration": "1 week",
            "language": "both",
            "difficulty": "beginner",
            "tags": "python, programming, tutorial"
        }
        
        try:
            response = self.session.post(f"{self.api_url}/skills/", json=skill_data)
            if response.status_code == 201:
                self.print_status("Test skill created successfully", "success")
                return response.json()
            else:
                self.print_status(f"Skill creation failed: {response.text}", "error")
                return None
        except Exception as e:
            self.print_status(f"Skill creation error: {str(e)}", "error")
            return None
    
    def run_comprehensive_test(self):
        """Run comprehensive API test"""
        self.print_status("🚀 Starting Comprehensive SkillSwap API Test", "info")
        print("=" * 60)
        
        # Test Swagger documentation
        self.test_swagger_endpoints()
        print()
        
        # Test public endpoints
        self.test_public_endpoints()
        print()
        
        # Register and login test user
        user_data = self.register_test_user()
        if user_data:
            if self.login_user(user_data['email'], user_data['password']):
                print()
                
                # Test protected endpoints
                self.test_protected_endpoints()
                print()
                
                # Create test skill
                self.create_test_skill()
        
        print("=" * 60)
        self.print_status("🎉 Comprehensive API Test Completed!", "success")
        print()
        self.print_status("📋 Important Links:", "info")
        print(f"   🌐 API Root: {self.base_url}/")
        print(f"   📚 Swagger UI: {self.base_url}/swagger/")
        print(f"   📖 ReDoc: {self.base_url}/redoc/")
        print(f"   ⚙️  Admin Panel: {self.base_url}/admin/")

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    tester = SkillSwapAPITester(base_url)
    tester.run_comprehensive_test()
