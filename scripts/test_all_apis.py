#!/usr/bin/env python
import os
import sys
import django
import requests
import json
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django with local settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings_local')
django.setup()

from django.contrib.auth import get_user_model
from skills.models import Category, Skill
from points.models import PointsPackage

User = get_user_model()

class APITester:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
        self.user_id = None
        
    def print_result(self, title, response):
        print(f"\n{'='*60}")
        print(f"🔍 {title}")
        print(f"{'='*60}")
        print(f"Status Code: {response.status_code}")
        print(f"URL: {response.url}")
        
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        except:
            print(f"Response: {response.text}")
    
    def setup_test_data(self):
        """Create test data"""
        print("🚀 Setting up test data...")
        
        # Create categories
        categories = [
            {'name': 'Programming', 'name_ar': 'البرمجة', 'description': 'Programming and software development'},
            {'name': 'Design', 'name_ar': 'التصميم', 'description': 'Graphic and web design'},
            {'name': 'Marketing', 'name_ar': 'التسويق', 'description': 'Digital marketing and advertising'},
            {'name': 'Writing', 'name_ar': 'الكتابة', 'description': 'Content writing and copywriting'},
        ]
        
        for cat_data in categories:
            Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
        
        # Create points packages
        packages = [
            {'name': 'Starter Pack', 'points': 100, 'price': 10.00},
            {'name': 'Pro Pack', 'points': 500, 'price': 45.00},
            {'name': 'Premium Pack', 'points': 1000, 'price': 80.00},
        ]
        
        for pkg_data in packages:
            PointsPackage.objects.get_or_create(
                name=pkg_data['name'],
                defaults=pkg_data
            )
        
        print("✅ Test data created successfully!")
    
    def test_authentication_apis(self):
        """Test Authentication APIs"""
        print("\n🔐 TESTING AUTHENTICATION APIs")
        
        # 1. Register a new user
        register_data = {
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        response = self.session.post(f'{self.base_url}/api/auth/register/', json=register_data)
        self.print_result("POST /api/auth/register/ - Register User", response)
        
        # 2. Login
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
        
        response = self.session.post(f'{self.base_url}/api/auth/login/', json=login_data)
        self.print_result("POST /api/auth/login/ - Login", response)
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get('tokens', {}).get('access')
            self.user_id = data.get('user', {}).get('id')
            if self.access_token:
                self.session.headers.update({'Authorization': f'Bearer {self.access_token}'})
        
        # 3. Get Profile
        response = self.session.get(f'{self.base_url}/api/auth/profile/')
        self.print_result("GET /api/auth/profile/ - View Profile", response)
        
        # 4. Update Profile
        update_data = {
            'bio': 'Updated bio for testing',
            'city': 'Cairo'
        }
        
        response = self.session.put(f'{self.base_url}/api/auth/profile/', json=update_data)
        self.print_result("PUT /api/auth/profile/ - Update Profile", response)
    
    def test_skills_apis(self):
        """Test Skills APIs"""
        print("\n🎯 TESTING SKILLS APIs")
        
        # 1. List categories
        response = self.session.get(f'{self.base_url}/api/skills/categories/')
        self.print_result("GET /api/skills/categories/ - List Categories", response)
        
        # 2. List skills
        response = self.session.get(f'{self.base_url}/api/skills/')
        self.print_result("GET /api/skills/ - List Skills", response)
        
        # 3. Create a new skill
        skill_data = {
            'category': 1,
            'title': 'Python Web Development',
            'description': 'I will create a Python web application for you',
            'points_required': 150,
            'estimated_duration': '3-5 days',
            'language': 'en',
            'difficulty': 'intermediate',
            'tags': 'python, django, web development'
        }
        
        response = self.session.post(f'{self.base_url}/api/skills/', json=skill_data)
        self.print_result("POST /api/skills/ - Create Skill", response)
        
        skill_id = None
        if response.status_code == 201:
            skill_id = response.json().get('id')
        
        # 4. Get skill details
        if skill_id:
            response = self.session.get(f'{self.base_url}/api/skills/{skill_id}/')
            self.print_result(f"GET /api/skills/{skill_id}/ - Skill Details", response)
        
        # 5. Search skills
        response = self.session.get(f'{self.base_url}/api/skills/?search=python')
        self.print_result("GET /api/skills/?search=python - Search Skills", response)
        
        # 6. Filter by category
        response = self.session.get(f'{self.base_url}/api/skills/?category=1')
        self.print_result("GET /api/skills/?category=1 - Filter by Category", response)
    
    def test_points_apis(self):
        """Test Points APIs"""
        print("\n💰 TESTING POINTS APIs")
        
        # 1. Get points packages
        response = self.session.get(f'{self.base_url}/api/points/packages/')
        self.print_result("GET /api/points/packages/ - Points Packages", response)
        
        # 2. Get transactions
        response = self.session.get(f'{self.base_url}/api/points/transactions/')
        self.print_result("GET /api/points/transactions/ - Transaction History", response)
        
        # 3. Get orders
        response = self.session.get(f'{self.base_url}/api/points/orders/')
        self.print_result("GET /api/points/orders/ - Orders List", response)
    
    def test_chat_apis(self):
        """Test Chat APIs"""
        print("\n💬 TESTING CHAT APIs")
        
        # 1. List chat rooms
        response = self.session.get(f'{self.base_url}/api/chat/')
        self.print_result("GET /api/chat/ - List Chat Rooms", response)
    
    def test_payments_apis(self):
        """Test Payments APIs"""
        print("\n💳 TESTING PAYMENTS APIs")
        
        # 1. Get payment history
        response = self.session.get(f'{self.base_url}/api/payments/')
        self.print_result("GET /api/payments/ - Payment History", response)
    
    def test_reviews_apis(self):
        """Test Reviews APIs"""
        print("\n⭐ TESTING REVIEWS APIs")
        
        # 1. List reviews
        response = self.session.get(f'{self.base_url}/api/reviews/')
        self.print_result("GET /api/reviews/ - List Reviews", response)
    
    def test_notifications_apis(self):
        """Test Notifications APIs"""
        print("\n🔔 TESTING NOTIFICATIONS APIs")
        
        # 1. List notifications
        response = self.session.get(f'{self.base_url}/api/notifications/')
        self.print_result("GET /api/notifications/ - List Notifications", response)
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting SkillSwap API Testing")
        print(f"Base URL: {self.base_url}")
        print(f"Time: {datetime.now()}")
        
        try:
            self.setup_test_data()
            self.test_authentication_apis()
            self.test_skills_apis()
            self.test_points_apis()
            self.test_chat_apis()
            self.test_payments_apis()
            self.test_reviews_apis()
            self.test_notifications_apis()
            
            print(f"\n{'='*60}")
            print("✅ API Testing Completed!")
            print(f"{'='*60}")
            
        except Exception as e:
            print(f"\n❌ Error during testing: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    tester = APITester()
    tester.run_all_tests()
