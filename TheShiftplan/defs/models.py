from django.db import models
from django.contrib.auth.models import Group, User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    worker = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} UserProfile, worker: {self.worker}'

    class Meta:
        ordering = ('worker',)


class SubCrew(models.Model):
    name = models.CharField('crew_name', max_length=200, unique=True, blank=False)
    description = models.TextField('description', null=True, blank=True, default='')
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name 


class Jobtype(models.Model):
    name = models.CharField('jobtype name', max_length=200)
    description = models.TextField('description', default='')  # former 
    default_rating = models.IntegerField(default=3)
    restricted_to_subcrew = models.BooleanField(default=False)
    subcrew = models.ForeignKey(SubCrew, on_delete=models.CASCADE, blank=True, null=True)
    
    def save(self, *args, **kwargs):            
        if not self.restricted_to_subcrew:
            self.subcrew = None
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'default_rating': self.default_rating,
            'restricted_to_subcrew': self.restricted_to_subcrew,
            'subcrew': self.subcrew
            }


class Job(models.Model):
    jobtype = models.ForeignKey(Jobtype, on_delete=models.CASCADE)
    begin_date = models.DateField('job begin date')
    end_date = models.DateField('job end date')
    begin_time = models.TimeField('job begin time')
    end_time = models.TimeField('job end time')
    rating = models.IntegerField('rating', null=True, blank=True)
    # during
    '''Default time formats: ['%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
 '%Y-%m-%d %H:%M',       # '2006-10-25 14:30'
 '%Y-%m-%d',             # '2006-10-25'
 '%m/%d/%Y %H:%M:%S',    # '10/25/2006 14:30:59'
 '%m/%d/%Y %H:%M',       # '10/25/2006 14:30'
 '%m/%d/%Y',             # '10/25/2006'
 '%m/%d/%y %H:%M:%S',    # '10/25/06 14:30:59'
 '%m/%d/%y %H:%M',       # '10/25/06 14:30'
 '%m/%d/%y']             # '10/25/06'
 '''
    def save(self, *args, **kwargs):
        if self.rating is None:
            self.rating = self.jobtype.default_rating
        super(Job, self).save(*args, **kwargs)

    def __str__(self):
        return "{jt_name} begin: {b}, {bt} end: {e}, {et}".format(jt_name=self.jobtype.name, b=self.begin_date, e=self.end_date, bt=self.begin_time, et=self.end_time)

    def as_dict(self):
        return {'begin_date': self.begin_date, 'end_date': self.end_date, "begin_time": self.begin_time, "end_time": self.end_time}