from django.contrib import admin
from django.conf import settings
from django.db.utils import OperationalError

from .signals import *

from .models import BiasHours, Workload
from defs.models import Shiftplan, Mode

try:
    shiftplan = Shiftplan.objects.all()[0]

    if shiftplan.mode.name == "assign_every_job":
        admin.site.register(BiasHours)
    elif shiftplan.mode.name in ("non_prioritized", "prioritized"):
        admin.site.register(Workload)
    # admin.site.register(Workload)
except:
    pass

if settings.DEBUG:
    from .models import UserOptions, UserJobRating
    admin.site.register(UserOptions)

    class UserJobRatingAdmin(admin.ModelAdmin):
        model = UserJobRating
        # That adds a “Filter” sidebar that lets people filter the change list by field:
        list_filter = ['user', 'job', 'rating']
        # That adds a search box at the top of the change list.
        search_fields = ['user', 'job', 'rating']

    admin.site.register(UserJobRating, UserJobRatingAdmin)