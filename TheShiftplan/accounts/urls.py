from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'accounts'
urlpatterns = [
    # path('', index_view, name='index'),
    path('register/', registration_view, name='register'),
]
