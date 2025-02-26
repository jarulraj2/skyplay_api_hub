from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User  # Import your custom User model

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active', 'created_by')  # Show created_by
    readonly_fields = ('created_by',)  # Make it non-editable

    fieldsets = UserAdmin.fieldsets + (  # Add created_by to the user form
        (_("Additional Info"), {"fields": ("created_by",)}),
    )

    def save_model(self, request, obj, form, change):
        """Set created_by only for new users"""
        if not obj.created_by:
            obj.created_by = request.user
        obj.save()

    def get_queryset(self, request):
        """Filter users based on role"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:  
            return qs  # Admin sees all users
        return qs.filter(created_by=request.user)  # Operators see only users they created

admin.site.register(User, CustomUserAdmin)  # Register user model
