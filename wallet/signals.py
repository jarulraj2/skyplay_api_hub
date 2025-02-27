from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Wallet
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:  # Create wallet only for operators
        Wallet.objects.create(user=instance)
