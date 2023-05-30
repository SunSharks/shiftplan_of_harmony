from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'sols'
urlpatterns = [
    path('', index_view, name='index'),
    path('admin_new_solutions/', admin_new_solutions_view, name='admin_solutions'),
    path('show_solution/<int:pk>', show_solution_view, name='show_solution'),
]
