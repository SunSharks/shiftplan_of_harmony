from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'prefs'
urlpatterns = [
    path('', chart_view, name='chart'),
    path('user_options/', user_options_view, name='user_options'),
    path('user_options/user_options_form/', user_options_form, name='user_options_form'),
    path('user_options/update', update_user_options, name='update_user_options'),
    # path('user_options/detail', user_options_detail, name='user_options_detail'),
    # path('<int:pk>/', tab_view, name='tab'),
]

