from django.db import models

class PaymentLog(models.Model):
    client_id = models.CharField(max_length=255, null=True, blank=True)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default="INR")
    device_id = models.CharField(max_length=255, null=True, blank=True)
    pack_or_channel_id = models.CharField(max_length=255, null=True, blank=True)
    request_data = models.JSONField(null=True, blank=True)
    response_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
