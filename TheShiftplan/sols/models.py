from django.db import models

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from defs.models import Job


class SolutionRun(models.Model):
    timestamp = models.DateTimeField("solution run timestamp", unique=True)
    final = models.BooleanField(default=False)

    def __str__(self):
        s = f"{self.final} {self.timestamp}"
        return s


class Solution(models.Model):
    solution_run = models.ForeignKey(SolutionRun, on_delete=models.CASCADE)
    final = models.BooleanField(default=False)

    def __str__(self):
        s = f"final: {self.final}"
        return s


class UserJobAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    assigned = models.BooleanField(default=False)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)

    def __str__(self):
        s = f"user: {self.user.username} job: {self.job} assigned: {self.assigned}"
        return s

    def as_dict(self):
        return {'user': self.user.pk, 'job': self.job.pk, 'assigned': self.assigned}

    class Meta:
        indexes = [
            models.Index(fields=["user", "job"]),
        ]