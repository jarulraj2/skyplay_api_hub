from django.contrib import admin
from .models import PaymentLog, Activation, Deactivation

class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ("client_id", "client_name", "amount", "currency", "device_id", "pack_or_channel_id", "created_at")
    readonly_fields = ("client_id", "client_name", "amount", "currency", "device_id", "pack_or_channel_id", "request_data", "response_data", "created_at")
    
    search_fields = ("client_id", "client_name", "device_id", "pack_or_channel_id")  # 🔍 Enable search

    list_filter = ("client_id", 'client_name', "created_at", "device_id", "pack_or_channel_id")  # 🏷️ Filter options
    
    def has_add_permission(self, request):
        return False  # ❌ Disable the "Add" button in admin

    def has_change_permission(self, request, obj=None):
        return False  # ❌ Disable editing logs in admin

    # def has_delete_permission(self, request, obj=None):
    #     return False  # ❌ Disable delete option in admin

# Register PaymentLog in admin
admin.site.register(PaymentLog, PaymentLogAdmin)

# Set a custom header, title, and index title for the admin site
admin.site.site_header = "Skyplay API Hub"
admin.site.site_title = "Skyplay API Hub"
admin.site.index_title = "Welcome to Skyplay API Hub"




class ActivationAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'channel_id', 'end_date', 'device_id')  # Use actual model fields
    search_fields = ('client_id', 'channel_id', 'device_id')
    list_filter = ('end_date',)
    class Media:
        js = ('js/admin_activation.js',)  # Path to your script

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            print("Error saving Activation:", e)
            raise e
admin.site.register(Activation, ActivationAdmin)


class DeactivationAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'channel_id', 'deactivated_at', 'deactivated_by', 'status')  # Display deactivation details
    search_fields = ('client_id', 'channel_id', 'deactivated_by__username')  # Search by deactivated_by (username)
    list_filter = ('end_date', 'status', 'deactivated_at', 'deactivated_by')  # Filter by deactivation time and user

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Optional: You could filter the queryset based on the logged-in user or other criteria
        return queryset

admin.site.register(Deactivation, DeactivationAdmin)
