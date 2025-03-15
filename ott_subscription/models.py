from django.db import models
from django.core.validators import FileExtensionValidator

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

    # ForeignKey to link OTT to an OTTPlan (One plan can have many OTTs)
    ott_plan = models.ForeignKey('OTTPlan', related_name='ott_plans', on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    

# Define the OTT Plan Model
class OTTPlan(models.Model):
    PLATFORM_CHOICES = [
        ('watcho', 'Watcho'),
        ('play_box', 'Play Box'),
        ('hotstar', 'Hotstar'),
        ('ottplay', 'OTTplay'),
        ('tata_play_binge', 'Tata Play Binge'),
    ]

    PLAN_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)  # Ensuring the code is unique for each platform
    status = models.CharField(max_length=10, choices=PLAN_STATUS_CHOICES, default='active')

   # Many-to-many relationship between OTTPlan and OTT
    otts = models.ManyToManyField(OTT, related_name='ott_plans_associated')
    
    def __str__(self):
        return f"{self.platform} - {self.name}"
    
     # Method to get all active OTTs associated with this plan
    def get_active_otts(self):
        return self.otts.filter(is_active=True)

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
    


class OTTSubscription(models.Model):
    client_id = models.CharField(max_length=255)
    platform_id = models.CharField(max_length=255)
    plan_id = models.CharField(max_length=255)
    subscription_date = models.DateTimeField(auto_now_add=True)  # Track when the subscription is created

    def __str__(self):
        return f"Subscription for {self.client_id} on {self.platform_id} - Plan {self.plan_id}"
    


class OTTActivationLog(models.Model):
    client_id = models.CharField(max_length=255)
    platform_id = models.CharField(max_length=255)
    plan_id = models.CharField(max_length=255)
    activation_date = models.DateTimeField(auto_now_add=True)  # The date when the activation occurred
    status = models.CharField(max_length=50, default='Success')  # You can track status (Success/Failure)
    message = models.TextField(blank=True, null=True)  # Optional field to store any additional message (e.g., error message)

    def __str__(self):
        return f"Activation Log for {self.client_id} on {self.platform_id} - {self.plan_id}"
