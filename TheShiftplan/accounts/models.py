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


    def __str__(self):
        l = [("username", self.username),("forename", self.forename), ("surname", self.surname), ("email", self.email), ("candidates_list", self.candidates_list)]
        l = [i for i in l if not i[1] is None]
        s = ""
        for label, var in l:
            s += f"{label}: {var}\n"
        return s.rstrip()