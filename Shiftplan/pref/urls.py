from django.urls import path

from .views import *


app_name = 'pref'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', tab_view, name='tab'),
]
