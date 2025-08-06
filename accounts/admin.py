from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserSkill

class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    list_display = ('email', 'first_name', 'last_name', 'points_balance', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'bio', 'avatar')}),
        (_('Location'), {'fields': ('location',)}),
        (_('Points'), {'fields': ('points_balance',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'level', 'years_of_experience', 'is_verified')
    list_filter = ('level', 'is_verified', 'years_of_experience')
    search_fields = ('user__email', 'name')
    readonly_fields = ('created_at',)

admin.site.register(User, UserAdmin)
admin.site.register(UserSkill, UserSkillAdmin)
