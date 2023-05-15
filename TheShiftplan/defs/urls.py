from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'defs'
urlpatterns = [
    path('', index_view, name='index'),
    ### Jobtypes
    path('jts/', jobtype_def, name='jobtype_def'),
    path('jts/jt_form/', create_jobtype_form, name='jobtype-form'),
    # path('jts/create/', create_jobtype, name='create-jobtype'),
    path('jts/<int:pk>/update', update_jobtype, name='update-jobtype'),
    path('jts/<int:pk>/detail', detail_jobtype, name='detail-jobtype'),
    path('jts/<int:pk>/delete', delete_jobtype, name='delete-jobtype'),
    ### Jobs
    path('jts/<int:pk>/jobs/', job_def, name='job_def'),
    path('jts/jobs/job_form/', create_job_form, name='job-form'),
    # path('jts/<int:pk>/jobs/create/', create_job, name='create-job'),
    path('jts/jobs/<int:pk>/update', update_job, name='update-job'),
    path('jts/jobs/<int:pk>/detail', detail_job, name='detail-job'),
    path('jts/jobs/<int:pk>/delete', delete_job, name='delete-job'),
]

