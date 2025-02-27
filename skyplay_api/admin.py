from django.contrib import admin
from .models import APILog

# Custom Admin Site to reorder the app list
class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)

        # Find "Skyplay API" and move it to the end
        skyplay_api_app = None
        other_apps = []

        for app in app_list:
            if app["name"] == "skyplay_api":
                skyplay_api_app = app
            else:
                other_apps.append(app)

        # Ensure "Skyplay API" is moved to the last position
        if skyplay_api_app:
            other_apps.append(skyplay_api_app)

        return other_apps

# Instantiate the custom admin site
custom_admin_site = CustomAdminSite(name="custom_admin")

@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    list_display = ('user', 'endpoint', 'status_code', 'timestamp')  # Show user
    search_fields = ('user__username', 'endpoint', 'request_data', 'response_data')  # Enable searching by user
    ordering = ('-timestamp',)
