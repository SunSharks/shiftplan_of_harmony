from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'admin_prefs'
urlpatterns = [
    path('', admin_prefs_view, name='admin_prefs'),
]