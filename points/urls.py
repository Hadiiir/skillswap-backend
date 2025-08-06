from django.urls import path
from . import views

app_name = 'points'

urlpatterns = [
    # Points Packages
    path('packages/', views.PointsPackageListView.as_view(), name='packages'),
    
    # Transactions
    path('transactions/', views.PointsTransactionListView.as_view(), name='transactions'),
    
    # Orders
    path('orders/', views.OrderListCreateView.as_view(), name='orders'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/accept/', views.AcceptOrderView.as_view(), name='accept-order'),
    path('orders/<int:pk>/complete/', views.CompleteOrderView.as_view(), name='complete-order'),
    path('orders/<int:pk>/cancel/', views.CancelOrderView.as_view(), name='cancel-order'),
]
