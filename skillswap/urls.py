"""
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
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', 
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
