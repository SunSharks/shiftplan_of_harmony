from .models import BiasHours, UserOptions

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_models(sender, instance, created, **kwargs):
    if created:
        BiasHours.objects.create(user=instance)
        UserOptions.objects.create(user=instance)