from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh/', views.RefreshTokenView.as_view(), name='refresh'),
    
    # Profile
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    
    # User Skills
    path('skills/', views.UserSkillListCreateView.as_view(), name='user-skills'),
    path('skills/<int:pk>/', views.UserSkillDetailView.as_view(), name='user-skill-detail'),
]
