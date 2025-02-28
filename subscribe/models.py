from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

class PaymentLog(models.Model):
    client_id = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    device_id = models.CharField(max_length=255, null=True, blank=True)
    pack_or_channel_id = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    order_id = models.CharField(max_length=255, unique=True)
    request_data = models.JSONField(null=True, blank=True)
    response_data = models.JSONField(null=True, blank=True)
    varified_resonse = models.JSONField(null=True, blank=True)
    
    # ✅ New Status Fields
    status = models.CharField(max_length=50, default="PENDING")  # NEW FIELD
    final_status = models.CharField(max_length=50, default="PENDING") 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} - Status: {self.status}"
    

from django.utils.timezone import now  # ✅ Import this

class Activation(models.Model):
    client_id = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=255)
    end_date = models.DateField()
    device_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=now)  # ✅ Use `now()`, NOT auto_now_add

    def __str__(self):
        return self.client_id




class Deactivation(models.Model):
    client_id = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=255)
    end_date = models.DateField()
    device_id = models.CharField(max_length=255)
    deactivated_at = models.DateTimeField(default=timezone.now)
    deactivated_by =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    status = models.CharField(max_length=255, default='deactivated')