from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save


from defs.models import Shiftplan, Jobtype, Job

class UserJobRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    rating = models.IntegerField(default=3, blank=True, null=True)

    def __str__(self):
        s = "user: {} job: {} rating: {}".format(self.user, self.job, self.rating)
        return s

    def as_dict(self):
        return {'user': self.user, 'job': self.job, 'rating': self.rating}

    class Meta:
        indexes = [
            models.Index(fields=["user", "job"]),
        ]


class UserOptions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    min_break_hours = models.IntegerField(default=4, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile, break: {self.min_break_hours}'

    def as_dict(self):
        return {'user': self.user, 'min_break_hours': self.min_break_hours}

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)



# class Chart(models.Model):
#     name = models.CharField(max_length=200) 
#     start_date = models.DateField()
#     responsible = models.ForeignKey(User, on_delete=models.CASCADE)
#     week_number = models.CharField(max_length=2, blank=True)
#     finish_date = models.DateField()

# #string representation method
#     def __str__(self):
#         return str(self.name)
# #overiding the save method
#     def save(self, *args, **kwargs):
#         print(self.start_date.isocalendar()[1])
#         if self.week_number == "":
#             self.week_number = self.start_date.isocalendar()[1]
#         super().save(*args, **kwargs)