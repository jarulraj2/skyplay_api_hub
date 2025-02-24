from django.db import models

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
