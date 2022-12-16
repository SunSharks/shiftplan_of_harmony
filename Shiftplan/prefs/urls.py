from django.urls import path
from .views import *

app_name = 'prefs'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', chart_view, name='chart'),
    # path('<int:pk>/', tab_view, name='tab'),
]
