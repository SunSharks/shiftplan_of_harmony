from django.contrib import admin
from django.conf import settings

from .signals import *

from .models import BiasHours
admin.site.register(BiasHours)

if settings.DEBUG:
    from .models import UserOptions
    admin.site.register(UserOptions)