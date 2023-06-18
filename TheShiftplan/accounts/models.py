import logging

from django.db import models
from django.contrib.auth.models import User

    

class CandidatesList(models.Model):
    name = models.CharField('cand_list_name', max_length=200, unique=True, blank=False)
    file = models.FileField(upload_to="candidates_files")


class UserCandidate(models.Model):
    username = models.CharField('cand username', max_length=200, unique=True, blank=True, null=True)
    forename = models.CharField('cand forename', max_length=200, blank=True, null=True)
    surname = models.CharField('cand surname', max_length=200, blank=True, null=True)
    email = models.EmailField('cand email', blank=True, null=True)
    candidates_list = models.ForeignKey(CandidatesList, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        all_empty = True
        find_empty = lambda attr: attr is None or attr.strip() == ""
        for attr in [self.username, self.forename, self.surname, self.email]:
            if not find_empty(attr):
                all_empty = False
                break
        if not all_empty:
            super(UserCandidate, self).save(*args, **kwargs)
            if not self.pk:
                logging.info(f"Created new UserCandidate instance. {self}")
            else:
                logging.info(f"Updated UserCandidate instance {self}")
        else:
            logging.info("Not saving. All entries empty.")

    def __str__(self):
        if self.user:
            user = self.user
        else:
            user = "False"
        l = [("user", user),("username", self.username),("forename", self.forename), ("surname", self.surname), ("email", self.email), ("candidates_list", self.candidates_list)]
        l = [i for i in l if not i[1] is None]
        s = ""
        for label, var in l:
            s += f"{label}: {var}\n"
        return s.rstrip()

    def as_dict(self):
        return {
            'forename': self.forename, 
            'surname': self.surname, 
            "email": self.email, 
            "username": self.username
        }