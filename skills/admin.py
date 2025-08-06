from django.contrib import admin
from .models import Category, Skill, SkillImage, SkillFAQ

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

@admin.register(SkillImage)
class SkillImageAdmin(admin.ModelAdmin):
    list_display = ['skill', 'caption', 'order', 'created_at']
    list_filter = ['created_at']

@admin.register(SkillFAQ)
class SkillFAQAdmin(admin.ModelAdmin):
    list_display = ['skill', 'question', 'order', 'created_at']
    list_filter = ['created_at']
