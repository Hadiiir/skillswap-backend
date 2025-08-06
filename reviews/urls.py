from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # Reviews
    path('', views.ReviewListCreateView.as_view(), name='review-list'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    
    # Skill Reviews
    path('skills/<int:skill_id>/', views.SkillReviewsView.as_view(), name='skill-reviews'),
]
