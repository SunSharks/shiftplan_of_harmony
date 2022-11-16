from django.urls import path

from .views import *


app_name = 'defs'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # path('<int:pk>/', ShiftplanDefView.as_view(), name='shiftplan_def'),
    path('<int:pk>/', shiftplan_def, name='shiftplan_def'),
    path('<int:shiftplan_id>/time_def/', time_def, name='time-def'),
    # path('<int:pk>/ti/', time_interval_def, name='ti_def'),
    path('<int:pk>/ti/create/', create_time_interval, name='create_ti'),
    path('<int:pk>/jobtype/', jobtype_def, name='jobtype_def'),
    path('<int:pk>/jobtype/create/', create_jobtype, name='create_jobtype'),
    path('jobtype/create-jobtype-form/', create_jobtype_form, name='create-jobtype-form'),
    path('jobtype/<int:pk>/', detail_jobtype, name='detail-jobtype'),
    path('jobtype/<int:pk>/update/', update_jobtype, name='update-jobtype'),
    path('jobtype/<int:pk>/delete/', delete_jobtype, name='delete-jobtype'),
    path('<int:pk>/job', job_def, name='job_def'),
    path('<int:pk>/job/create/', create_job, name='create-job'),
    path('job/create-job-form/', create_job_form, name='create-job-form'),
    path('job/<int:pk>/', detail_job, name='detail-job'),
    path('job/<int:pk>/update/', update_job, name='update-job'),
    path('job/<int:pk>/delete/', delete_job, name='delete-job'),
]
