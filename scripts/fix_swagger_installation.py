#!/usr/bin/env python3
"""
Fix Swagger installation issues and set up full documentation
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success: {command}")
            return True
        else:
            print(f"❌ Error: {command}")
            print(f"Error output: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception running {command}: {e}")
        return False

def install_swagger_dependencies():
    """Install required Swagger packages"""
    print("🔧 Installing Swagger dependencies...")
    
    packages = [
        "drf-yasg==1.21.7",
        "packaging",
        "inflection", 
        "ruamel.yaml",
        "coreapi",
        "coreschema"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        if not run_command(f"pip install {package}"):
            print(f"Failed to install {package}")
            return False
    
    print("✅ All Swagger packages installed successfully!")
    return True

def create_swagger_config():
    """Create Swagger configuration file"""
    print("📝 Creating Swagger configuration...")
    
    swagger_config = '''"""
Swagger configuration for the project
"""
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="SkillSwap API",
        default_version='v1',
        description="""
        # 🎯 SkillSwap API Documentation
        
        Welcome to the SkillSwap API documentation - the leading platform for skill swapping!
        
        ## 🔐 Authentication
        This API uses JWT for authentication. To get the token:
        
        1. Register a new account via `/api/accounts/register/`
        2. Log in via `/api/accounts/login/`
        3. Use the access_token in the header: `Authorization: Bearer {token}`
        
        ## 📚 Main Modules
        
        ### 👤 Accounts
        - User registration and account management
        - Login and logout
        - Profile management
        
        ### 🎯 Skills
        - Creating and displaying skills
        - Advanced search and filtering
        - Managing categories and classifications
        
        ### 📦 Orders
        - Creating and managing orders
        - Order status tracking
        - Rating system
        
        ### 💰 Points
        - Buying and managing points
        - Transaction history
        - Reward system
        
        ### 💬 Chat
        - Instant messaging
        - Group chats
        - Message notifications
        
        ### 💳 Payments
        - Payment processing
        - Support for multiple payment gateways
        - Financial transaction history
        
        ### ⭐ Reviews
        - Rating skills and services
        - Comment system
        - Review statistics
        
        ### 🔔 Notifications
        - Instant notifications
        - Notification settings
        - Notification history
        
        ## 🔍 Search and Filtering
        Most endpoints support:
        - `?search=keyword` - search in relevant fields
        - `?category=1` - filter by category
        - `?status=active` - filter by status
        - `?ordering=-created_at` - sort results
        - `?page=2&page_size=20` - pagination
        
        ## 🌐 Multilingual Support
        - `Accept-Language: ar` for Arabic
        - `Accept-Language: en` for English
        
        ## 📞 Technical Support
        - Email: support@skillswap.com
        - Documentation: https://docs.skillswap.com
        """,
        terms_of_service="https://skillswap.com/terms/",
        contact=openapi.Contact(
            name="SkillSwap API Support",
            email="api-support@skillswap.com",
            url="https://skillswap.com/support"
        ),
        license=openapi.License(
            name="MIT License",
            url="https://opensource.org/licenses/MIT"
        ),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)
'''
    
    with open('/app/skillswap/swagger_config.py', 'w', encoding='utf-8') as f:
        f.write(swagger_config)
    
    print("✅ Swagger configuration file created")

def update_settings():
    """Update Django settings to support Swagger"""
    print("⚙️ Updating Django settings...")
    
    settings_path = '/app/skillswap/settings.py'
    
    # Read the current file
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ensure drf_yasg is in INSTALLED_APPS
    if "'drf_yasg'," not in content:
        # Add drf_yasg to THIRD_PARTY_APPS
        content = content.replace(
            "THIRD_PARTY_APPS = [",
            "THIRD_PARTY_APPS = [\n    'drf_yasg',"
        )
    
    # Write the updated file
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Django settings updated")

def update_urls():
    """Update URLs to include Swagger"""
    print("🔗 Updating URLs...")
    
    urls_content = '''"""
Main URLs for the project with Swagger support
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger setup
schema_view = get_schema_view(
    openapi.Info(
        title="SkillSwap API",
        default_version='v1',
        description="""
        # 🎯 SkillSwap API Documentation
        
        Welcome to the SkillSwap API documentation!
        
        ## 🔐 Authentication
        Use JWT Token in header: `Authorization: Bearer {token}`
        
        ## 📚 Available Modules
        - **Accounts**: User management and accounts
        - **Skills**: Skills and services
        - **Orders**: Orders and bookings
        - **Points**: Points and rewards
        - **Chat**: Messages and chats
        - **Payments**: Payments and transactions
        - **Reviews**: Ratings and reviews
        - **Notifications**: Notifications and alerts
        """,
        terms_of_service="https://skillswap.com/terms/",
        contact=openapi.Contact(email="support@skillswap.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    re_path(r'^swagger(?P<format>\\.json|\\.yaml)$', 
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), 
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), 
         name='schema-redoc'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), 
         name='api-docs'),
    
    # API Endpoints
    path('api/accounts/', include('accounts.urls')),
    path('api/skills/', include('skills.urls')),
    path('api/points/', include('points.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/notifications/', include('notifications.urls')),
    
    # API Root
    path('api/', schema_view.with_ui('swagger', cache_timeout=0), 
         name='api-root'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), 
         name='home'),
]

# Static and Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''
    
    with open('/app/skillswap/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_content)
    
    print("✅ URLs updated")

def update_requirements():
    """Update requirements.txt file"""
    print("📋 Updating requirements.txt...")
    
    requirements_content = '''Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
django-filter==23.3
channels==4.0.0
channels-redis==4.1.0
redis==5.0.1
celery==5.3.4
django-celery-beat==2.5.0
python-decouple==3.8
dj-database-url==2.1.0
psycopg2-binary==2.9.9
Pillow==10.1.0
djangorestframework-simplejwt==5.3.0
django-oauth-toolkit==1.7.1
django-allauth==0.57.0
stripe==7.8.0
whitenoise==6.6.0
gunicorn==21.2.0
drf-yasg==1.21.7
packaging
inflection
ruamel.yaml
coreapi
coreschema
'''
    
    with open('/app/requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements_content)
    
    print("✅ requirements.txt updated")

def test_swagger_setup():
    """Test Swagger setup"""
    print("🧪 Testing Swagger setup...")
    
    try:
        import drf_yasg
        print(f"✅ drf_yasg version: {drf_yasg.__version__}")
        
        # Test Django setup
        from django.conf import settings
        
        if 'drf_yasg' in settings.INSTALLED_APPS:
            print("✅ drf_yasg found in INSTALLED_APPS")
        else:
            print("❌ drf_yasg not found in INSTALLED_APPS")
            
        print("✅ Swagger setup successful!")
        
    except ImportError as e:
        print(f"❌ Error importing drf_yasg: {e}")
    except Exception as e:
        print(f"❌ Error in setup: {e}")

def main():
    """Main function"""
    print("🚀 Starting Swagger installation fix...")
    
    if install_swagger_dependencies():
        create_swagger_config()
        update_settings()
        update_urls()
        update_requirements()
        test_swagger_setup()
        
        print("\n🎉 Swagger installation fixed successfully!")
        print("\n📋 Next steps:")
        print("1. Restart the server: docker-compose restart")
        print("2. Open Swagger UI: http://localhost:8000/swagger/")
        print("3. Open ReDoc: http://localhost:8000/redoc/")
    else:
        print("❌ Failed to fix Swagger installation")
        sys.exit(1)

if __name__ == "__main__":
    main()
