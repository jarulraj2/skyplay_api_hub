from django.contrib import admin
from .models import OTTPlan, SkylinkPlan, OTTActivationLog, OTT
from django.utils.html import mark_safe



class OTTAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'image_tag')  # Show the image in the list view
    list_filter = ('is_active',)  # Filter by active status
    search_fields = ('name',)  # Allow search by name

    # Image display method
    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return 'No Image'
    
    # Make the image field readonly in the form but editable for upload
    readonly_fields = ('image_tag',)  # Make sure image_tag is readonly in the form

    # Make the image field editable in the form view (not readonly)
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'is_active', 'image'),
        }),
    )


# Admin configuration for the OTTPlan model
class OTTPlanAdmin(admin.ModelAdmin):
    list_display = ('platform', 'name', 'code', 'status')
    list_filter = ('platform', 'status')  # Add filter by platform and status
    search_fields = ('name', 'code')  # Add search functionality by name and code
    filter_horizontal = ('otts',) 
    # This would show the related OTTs in the plan view (optional)
    # This assumes that `otts` is the related name set on the ForeignKey in the OTT model
    def get_otts(self, obj):
        return ", ".join([ott.name for ott in obj.otts.all()])  # Display OTT names associated with the plan
    get_otts.short_description = 'OTTs'

# Register the OTTPlan and OTT models to the admin
admin.site.register(OTTPlan, OTTPlanAdmin)
admin.site.register(OTT, OTTAdmin)

# Existing SkylinkPlanAdmin for your SkylinkPlan model
class SkylinkPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status')
    filter_horizontal = ('ott_plans',)  # This will allow multiple selection in the admin

admin.site.register(SkylinkPlan, SkylinkPlanAdmin)

# Existing OTTActivationLogAdmin
class OTTActivationLogAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'platform_id', 'plan_id', 'activation_date', 'status', 'message')
    list_filter = ('status', 'platform_id')
    search_fields = ('client_id', 'platform_id', 'plan_id')
    ordering = ('-activation_date',)
    date_hierarchy = 'activation_date'  # Adds date-based filtering

admin.site.register(OTTActivationLog, OTTActivationLogAdmin)
