from django.db import models


class Shiftplan(models.Model):
    name = models.CharField('shiftplan_name', max_length=200, unique=True, blank=False, default="")
    time_format = models.CharField("time_format", max_length=50, default="hourly")

    def __str__(self):
        return self.name

# class Subgroup(models.Model):
#     shiftplan = models.ForeignKey(Shiftplan, on_delete=models.CASCADE)
#     name = models.CharField('subgroup name', max_length=200)
#
#     def __str__(self):
#         return self.name
#
#
# class Day(models.Model):
#     shiftplan = models.ForeignKey(Shiftplan, on_delete=models.CASCADE)
#     name = models.CharField('day name', max_length=200)
#     date = models.DateField('date')
#
#     def __str__(self):
#         return str(self.date)


class Jobtype(models.Model):
    shiftplan = models.ForeignKey(Shiftplan, on_delete=models.CASCADE)
    name = models.CharField('jobtype name', max_length=200)
    # subgroup = models.ForeignKey(Subgroup, on_delete=models.CASCADE)
    description = models.TextField('description', default='')  # former "competences"

    def __str__(self):
        return self.name


class Job(models.Model):
    jobtype = models.ForeignKey(Jobtype, on_delete=models.CASCADE)
    begin = models.DateTimeField('job begin')
    end = models.DateTimeField('job end')
    # during

    def __str__(self):
        return "Job"

#
#
#
# CREATE TABLE Users (
#     id           INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#     fullname_id  INT                NOT NULL UNIQUE,
#     pw           VARCHAR(255)       NOT NULL,
#     nickname     VARCHAR(255)       NOT NULL UNIQUE,
#     email        VARCHAR(255)       NULL,
#     bias         INT                NOT NULL DEFAULT 0,
#     break        INT                NOT NULL DEFAULT 4
# );
#
# CREATE TABLE Names (
#   id         INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#   surname    VARCHAR(255)     NOT NULL,
#   famname    VARCHAR(255)     NOT NULL,
#   registered BOOLEAN          NULL DEFAULT 0,
#   helper     BOOLEAN          NOT NULL DEFAULT 0
# );
#
# CREATE TABLE Helpers (
#   id           INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#   fullname_id  INT                NOT NULL UNIQUE,
#   pw           VARCHAR(255)       NOT NULL,
#   nickname     VARCHAR(255)       NOT NULL UNIQUE,
#   email        VARCHAR(255)       NULL,
#   ticketnumber INT                NULL UNIQUE,
#   workload     INT                NOT NULL DEFAULT 4,
#   break        INT                NOT NULL DEFAULT 4
# );
