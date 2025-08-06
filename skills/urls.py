from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Skills
    path('', views.SkillListCreateView.as_view(), name='skill-list'),
    path('<int:pk>/', views.SkillDetailView.as_view(), name='skill-detail'),
]
