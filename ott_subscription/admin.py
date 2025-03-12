from django.contrib import admin
from .models import OTTPlan, SkylinkPlan

class OTTPlanAdmin(admin.ModelAdmin):
    list_display = ('platform', 'name', 'code')
    list_filter = ('platform',)  # Add a filter by platform
    search_fields = ('name', 'code')  # Optional: Add search functionality

admin.site.register(OTTPlan, OTTPlanAdmin)


class SkylinkPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status')
    filter_horizontal = ('ott_plans',)  # This will allow multiple selection in the admin

admin.site.register(SkylinkPlan, SkylinkPlanAdmin)
