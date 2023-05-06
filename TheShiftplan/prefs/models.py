from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save


from defs.models import Jobtype, Job

class UserJobRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    rating = models.IntegerField(default=3, blank=True, null=True)

    def __str__(self):
        s = "user: {} job: {} rating: {}".format(self.user.username, self.job, self.rating)
        return s

    def as_dict(self):
        return {'user': self.user.pk, 'job': self.job.pk, 'rating': self.rating}

    class Meta:
        indexes = [
            models.Index(fields=["user", "job"]),
        ]


class UserOptions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    min_break_hours = models.IntegerField(default=4, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} UserOptions, break: {self.min_break_hours}'

    def as_dict(self):
        return {
            'user': self.user.pk,
            'min_break_hours': self.min_break_hours
        }

class BiasHours(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bias_hours = models.IntegerField(default=0, blank=True, null=True)
    explanation = models.TextField(default="", blank=True, null=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} BiasHours, bias: {self.bias_hours}, explanation: {self.explanation}'