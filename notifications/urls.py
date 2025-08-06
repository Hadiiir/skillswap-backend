from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Notifications
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/read/', views.MarkAsReadView.as_view(), name='mark-as-read'),
    path('read-all/', views.MarkAllAsReadView.as_view(), name='mark-all-as-read'),
]
