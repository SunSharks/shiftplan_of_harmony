from django.contrib import admin
from django.conf import settings

from .signals import *

from .models import BiasHours
admin.site.register(BiasHours)

if settings.DEBUG:
    from .models import UserOptions, UserJobRating
    admin.site.register(UserOptions)
    admin.site.register(UserJobRating)