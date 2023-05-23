from django.contrib import admin
from django.conf import settings

from .signals import *

from .models import BiasHours#, Workload
admin.site.register(BiasHours)
# admin.site.register(Workload)


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