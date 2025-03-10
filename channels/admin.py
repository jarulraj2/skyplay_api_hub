from django.contrib import admin
from import_export import resources
from import_export.admin import ImportMixin, ExportMixin
from .models import Channel

class ChannelResource(resources.ModelResource):
    class Meta:
        model = Channel
        exclude = ('id',)  # Exclude the 'id' field from both import and export

    def before_import_row(self, row, **kwargs):
        # If the 'id' column is present in the import file, remove it
        if 'id' in row:
            del row['id']
        return row

    def get_instance(self, instance_loader, row):
        """
        Override this method to check for the `channel_id` and update the instance 
        if it exists, or create a new one if it doesn't.
        """
        # Try to find an existing Channel instance based on the `channel_id` from the row
        channel_id = row.get('channel_id')
        if channel_id:
            try:
                return Channel.objects.get(channel_id=channel_id)  # Find existing Channel by channel_id
            except Channel.DoesNotExist:
                return None  # If not found, create a new one
        return None

# Channel Admin class with both Import and Export functionality
class ChannelAdmin(ImportMixin, ExportMixin, admin.ModelAdmin):
    list_display = ('channel_id', 'channel_name', 'price')  # Fields to display in the admin panel
    resource_class = ChannelResource  # Attach the resource for import/export

# Register the model with the admin panel
admin.site.register(Channel, ChannelAdmin)
