from django.urls import path

from . import views


app_name = 'defs'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:shiftplan_id>/', views.shiftplan_def, name='shiftplan_def'),
    path('<int:shiftplan_id>/time_def/', views.time_def, name='time-def'),
    path('<int:shiftplan_id>/jobtype_def/', views.jobtype_def, name='jobtype_def'),
    path('<int:shiftplan_id>/job_def/', views.job_def, name='job_def'),
]
