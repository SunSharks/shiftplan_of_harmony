from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'sols'
urlpatterns = [
    path('', index_view, name='index'),
    path('sol_runs/', sol_runs_view, name='sol_runs'),
    path('admin_new_solutions/<int:pk>/', admin_solutions_view, name='admin_solutions'),
    path('show_solution/<int:pk>/', show_solution_view, name='show_solution'),
    path('set_final_sol_run/<int:pk>/', set_sol_run_final_view, name='set_sol_run_final'),
    path('unset_final_sol_run/', unset_sol_run_final_view, name='unset_sol_run_final'),
    path('set_final_sol/<int:pk>/', set_sol_final_view, name='set_sol_final'),
    path('unset_final_sol/<int:pk>/', unset_sol_final_view, name='unset_sol_final')
]
