from django.contrib import admin
from .models import OTTPlan, SkylinkPlan, OTTActivationLog, OTT, OTTAggregator
from django.utils.html import mark_safe
from django.utils.html import format_html
import json

# Admin configuration for the OTT model
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

admin.site.register(OTT, OTTAdmin)

# Admin configuration for OTTAggregator model
class OTTAggregatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status')  # Display name, code, and status
    list_filter = ('status',)  # Filter by status (active/inactive)
    search_fields = ('name', 'code')  # Allow search by name or code
    list_editable = ('status',)  # Allow editing the status directly from the list view

admin.site.register(OTTAggregator, OTTAggregatorAdmin)


# Admin configuration for the OTTPlan model
class OTTPlanAdmin(admin.ModelAdmin):
    list_display = ('get_platform', 'name', 'code', 'status', 'get_otts', 'price')  # Add price to the display
    list_filter = ('platform_id', 'status')  # Filter by platform_id and status
    search_fields = ('name', 'code', 'platform_id__name')  # Search by platform's name, name, and code
    filter_horizontal = ('otts',)  # Allow multiple OTT selection in horizontal view

    # Display OTT names associated with the plan
    def get_otts(self, obj):
        return ", ".join([ott.name for ott in obj.otts.all()])  # Assuming 'name' is a field in the OTT model
    get_otts.short_description = 'OTTs'

    # Display the platform's name (from OTTAggregator)
    def get_platform(self, obj):
        return obj.platform_id.name  # Use platform_id to reference OTTAggregator
    get_platform.admin_order_field = 'platform_id__name'  # Sorting by platform's name
    get_platform.short_description = 'Platform'  # Label for the admin list view

    # Add price field to the list display
    def price(self, obj):
        return obj.price  # Ensure price is a field in your model
    price.short_description = 'Price'  # Label for the price column in the admin view

    # Filter active platforms in the form
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "platform_id":  # Correct foreign key field name
            kwargs["queryset"] = OTTAggregator.objects.filter(status='active')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(OTTPlan, OTTPlanAdmin)


# Admin configuration for the SkylinkPlan model
class SkylinkPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status')
    filter_horizontal = ('ott_plans',)  # This will allow multiple selection in the admin

admin.site.register(SkylinkPlan, SkylinkPlanAdmin)


# Admin configuration for OTTActivationLog model

# Admin configuration for OTTActivationLog model
class OTTActivationLogAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the list view
    list_display = (
        'client_id', 
        'platform_id', 
        'plan_id', 
        'activation_date', 
        'expiration_date',
        'status', 
        'message', 
        'subscription_tiers_display',  # Add a custom field for displaying subscription_tiers
        'amount_display'  # Add a custom field for displaying amount if 'paid'
    )
    
    list_filter = ('status', 'platform_id', 'subscription_tiers')  # Filter by subscription_tiers
    search_fields = ('client_id', 'platform_id', 'plan_id')
    ordering = ('-activation_date',)
    date_hierarchy = 'activation_date'  # Adds date-based filtering

    # Method to display 'subscription_tiers' (free/paid)
    def subscription_tiers_display(self, obj):
        return obj.subscription_tiers.capitalize()  # Capitalize 'free' or 'paid'
    subscription_tiers_display.short_description = 'Subscription Tier'

    # Method to display the amount for 'paid' subscription
    def amount_display(self, obj):
        if obj.subscription_tiers == 'paid':
            # Assuming the payment_amount is stored in INR and you want to display it with the currency
            return f"{obj.payment_amount} {obj.payment_currency.upper()}"
        return '-'
    amount_display.short_description = 'Amount (Currency)'

    # Custom method to format 'input' JSON for display
    def formatted_input(self, obj):
        try:
            input_data = json.loads(obj.input)
            formatted_input = json.dumps(input_data, indent=2)
            return format_html('<pre>{}</pre>', formatted_input)
        except (ValueError, TypeError):
            return 'Invalid JSON or Empty'
    formatted_input.short_description = 'Formatted Input'

    # Custom method to format 'output' JSON for display
    def formatted_output(self, obj):
        try:
            output_data = json.loads(obj.output)  # Parse string into dictionary
            formatted_output = json.dumps(output_data, indent=2)  # Pretty-print JSON with indentation
            return format_html('<pre>{}</pre>', formatted_output)  # Wrap in <pre> tags for better formatting
        except (ValueError, TypeError):
            return 'Invalid JSON or Empty'
    formatted_output.short_description = 'Formatted Output'

    # Include formatted fields in the readonly view and exclude input/output for editing
    exclude = ('input', 'output',)
    readonly_fields = ('formatted_input', 'formatted_output', 'subscription_tiers_display', 'amount_display')

    # Disable editing of payment-related fields for 'paid' subscriptions
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj and obj.subscription_tiers == 'paid':
            # Add payment fields to readonly if the subscription is 'paid'
            readonly_fields += ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'payment_amount', 'payment_currency')
        return readonly_fields

admin.site.register(OTTActivationLog, OTTActivationLogAdmin)

