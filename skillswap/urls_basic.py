"""
Basic URL configuration for SkillSwap project
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'message': 'Welcome to SkillSwap API',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'accounts': '/api/accounts/',
            'skills': '/api/skills/',
            'points': '/api/points/',
            'reviews': '/api/reviews/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api-root'),
    path('api/', api_root, name='api-root'),
    path('api/accounts/', include('accounts.urls')),
    path('api/skills/', include('skills.urls')),
    path('api/points/', include('points.urls')),
    path('api/reviews/', include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
