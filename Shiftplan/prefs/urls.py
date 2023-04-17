from django.urls import path
from .views import *

app_name = 'prefs'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', chart_view, name='chart'),
    path('user_options/', user_options_view, name='user_options'),
    path('user_options/user_options_form/', user_options_form, name='user_options_form'),
    path('user_options/detail', user_options_detail, name='user_options_detail'),
    # path('<int:pk>/', tab_view, name='tab'),
]
