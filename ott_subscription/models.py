from django.db import models
from django.core.validators import FileExtensionValidator
from decimal import Decimal 
from django.utils import timezone
from datetime import timedelta
from datetime import datetime, timedelta
    # Function to calculate expiration date (current date + 30 days)
def get_expiration_date():
    return timezone.now() + timedelta(days=30)


# Define OTTAggregator Model
class OTTAggregator(models.Model):
    PLATFORM_CHOICES = [
        ('watcho', 'Watcho'),
        ('play_box', 'Play Box'),
        ('hotstar', 'Hotstar'),
        ('ottplay', 'OTTplay'),
        ('tata_play_binge', 'Tata Play Binge'),
    ]

    name = models.CharField(max_length=100, unique=True)  # Name of the aggregator
    code = models.CharField(max_length=50, unique=True)  # Unique code for the aggregator
    status = models.CharField(
        max_length=50, 
        choices=[('active', 'Active'), ('inactive', 'Inactive')], 
        default='active'
    )  # Status can be 'active' or 'inactive'

    def __str__(self):
        return self.name  # Returns the name of the aggregator

    class Meta:
        verbose_name = 'OTT Aggregator'
        verbose_name_plural = 'OTT Aggregators'


# Define the OTT Model
class OTT(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)  # Ensure the 'code' field is unique
    is_active = models.BooleanField(default=True)
    image = models.ImageField(
        upload_to='ott_images/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )

    ott_plan = models.ForeignKey('OTTPlan', related_name='ott_plans', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


# Define the OTT Plan Model
class OTTPlan(models.Model):
    PLAN_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    platform_id = models.ForeignKey(OTTAggregator, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)  # Ensuring the code is unique for each platform
    status = models.CharField(max_length=10, choices=PLAN_STATUS_CHOICES, default='active')
    # New price field to store the price of the plan
    price = models.DecimalField(
        max_digits=10,  # Total number of digits allowed (e.g., for 99999999.99)
        decimal_places=2,  # Number of decimal places (e.g., for .99 cents)
        default=Decimal('0.00')  # Default price is 0.00 (you can adjust this if needed)
    )
    otts = models.ManyToManyField(OTT, related_name='ott_plans_associated')  # Many-to-many with OTT

    def __str__(self):
        return f"{self.platform_id.name} - {self.name}"  # Fix the __str__ method

    def get_active_otts(self):
        return self.otts.filter(is_active=True)  # Get active OTTs related to the plan


# Define the Skylink Plan Model
class SkylinkPlan(models.Model):
    PLAN_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)  # Ensuring the plan code is unique
    ott_plans = models.ManyToManyField(OTTPlan)  # Many-to-many relationship with OTTPlans
    status = models.CharField(max_length=10, choices=PLAN_STATUS_CHOICES, default='active')
    

    def __str__(self):
        return self.name


# Define the OTTSubscription Model
class OTTSubscription(models.Model):
    client_id = models.CharField(max_length=255)
    platform_id = models.ForeignKey(OTTAggregator, on_delete=models.CASCADE)  # Us
    plan_id = models.CharField(max_length=255)
    subscription_date = models.DateTimeField(auto_now_add=True)  # Track when the subscription is created

    def __str__(self):
        return f"Subscription for {self.client_id} on {self.platform_id} - Plan {self.plan_id}"


# Define the OTTActivationLog Model
class OTTActivationLog(models.Model):
    client_id = models.CharField(max_length=255)
    platform_id = models.ForeignKey(OTTAggregator, on_delete=models.CASCADE)  # Us
    plan_id = models.CharField(max_length=255)
    activation_date = models.DateTimeField(auto_now_add=True)  # The date when the activation occurred
    status = models.CharField(max_length=50, default='Success')  # Track status like Success/Failure
    message = models.TextField(blank=True, null=True)  # Optional field for any additional message

    input = models.JSONField(null=True, blank=True)  # Store request data
    response_status = models.IntegerField(null=True, blank=True)  # Store response status
    output = models.JSONField(null=True, blank=True)  # Store response body as JSON
    endpoint = models.CharField(null=True, blank=True, max_length=5000)  # Endpoint used in the request

    # Add the subscription_tiers field here
    subscription_tiers = models.CharField(max_length=50, default='free')

     # Payment details for paid subscriptions
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    payment_verified = models.BooleanField(default=False)

    # New field to store the payment amount for paid subscriptions
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_currency = models.CharField(max_length=10, blank=True, null=True)

       # New field to store the expiration date (current date + 30 days)
    expiration_date = models.DateTimeField(default=get_expiration_date)

    def __str__(self):
        return f"Activation Log for {self.client_id} on {self.platform_id} - {self.plan_id}"
    

  

class VerificationCode(models.Model):
    email = models.EmailField(unique=True, blank=True, null=True)  # Email can be null if it's a phone number verification
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Phone number can be stored as well
    code = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        """Check if the verification code has expired"""
        expiry_time = self.timestamp + timedelta(minutes=10)  # Code is valid for 10 minutes
        
        # Use timezone-aware `timezone.now()` for the current time
        return timezone.now() > expiry_time  # Compare with timezone-aware current time