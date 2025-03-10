from django.contrib import admin
from import_export import resources
from import_export.admin import ImportMixin, ExportMixin  # Import both ImportMixin and ExportMixin
from .models import Channel

# Channel Resource for import/export
class ChannelResource(resources.ModelResource):
    class Meta:
        model = Channel

# Channel Admin class with both Import and Export functionality
class ChannelAdmin(ImportMixin, ExportMixin, admin.ModelAdmin):
    list_display = ('channel_id', 'channel_name', 'price')  # Fields to display in the admin panel
    resource_class = ChannelResource  # Attach the resource for import/export

# Register the model with the admin panel
admin.site.register(Channel, ChannelAdmin)
