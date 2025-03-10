# watcho/models.py
from django.db import models

class Encryption(models.Model):
    plain_text = models.TextField()  # Field for plain text input
    encrypted_text = models.TextField(blank=True, null=True)  # Field for storing encrypted text

    def __str__(self):
        return self.plain_text
