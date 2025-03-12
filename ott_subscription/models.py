from django.db import models

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
    def __str__(self):
        return f"{self.platform} - {self.name}"

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
    
