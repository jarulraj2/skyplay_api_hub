# channels/models.py

from django.db import models

class Channel(models.Model):
    # auto-increment ID is default in Django
    channel_id = models.CharField(max_length=100, unique=True)  # channel_id as a string, unique
    channel_name = models.CharField(max_length=255)  # name of the channel
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price with 2 decimal places


