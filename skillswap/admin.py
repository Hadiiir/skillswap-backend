from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from skills.models import Category, Skill, SkillImage, SkillFAQ
from points.models import PointsPackage, PointsTransaction, Order
from payments.models import Payment
from reviews.models import Review
from notifications.models import Notification

# Register Skills models
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_ar', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'name_ar']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'points_required', 'status', 'average_rating', 'created_at']
    list_filter = ['category', 'status', 'difficulty', 'language', 'is_featured']
    search_fields = ['title', 'title_ar', 'description', 'tags']
    readonly_fields = ['average_rating', 'total_reviews', 'total_orders']

# Register Points models
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

# Register other models
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['user__email', 'external_payment_id']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'reviewee', 'skill', 'rating', 'is_public', 'created_at']
    list_filter = ['rating', 'is_public', 'created_at']
    search_fields = ['reviewer__email', 'reviewee__email', 'skill__title']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__email', 'title', 'message']
