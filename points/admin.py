from django.contrib import admin
from .models import PointsPackage, PointsTransaction, Order

@admin.register(PointsPackage)
class PointsPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'points', 'price', 'discount_percentage', 'is_popular', 'is_active']
    list_filter = ['is_popular', 'is_active']

@admin.register(PointsTransaction)
class PointsTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'amount', 'status', 'created_at']
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = ['user__email', 'description']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'seller', 'skill', 'points_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['buyer__email', 'seller__email', 'skill__title']
