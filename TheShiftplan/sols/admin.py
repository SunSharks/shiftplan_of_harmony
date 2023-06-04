from django.contrib import admin

from .models import SolutionRun, Solution, UserJobAssignment
from .signals import *

admin.site.register(SolutionRun)
admin.site.register(Solution)
admin.site.register(UserJobAssignment)