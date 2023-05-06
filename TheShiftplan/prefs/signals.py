from .models import BiasHours, UserOptions, UserJobRating
from defs.models import Job

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        BiasHours.objects.create(user=instance)
        UserOptions.objects.create(user=instance)

        jobs = Job.objects.all()
        for j in jobs:
            UserJobRating.objects.create(user=instance, job=j, rating=j.rating)


@receiver(post_save, sender=Job)
def job_created(sender, instance, created, **kwargs):
    if created:
        users = User.objects.all()
        for u in users:
            UserJobRating.objects.create(user=u, job=instance, rating=instance.rating)


