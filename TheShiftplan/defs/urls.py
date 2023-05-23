from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'defs'
urlpatterns = [
    path('', index_view, name='index'),
    ### Jobtypes
    path('jts/', jobtype_def, name='jobtype_def'),
    path('jts/jt_form/', create_jobtype_form, name='jobtype-form'),
    path('jts/<int:pk>/visual_job_def/', visual_job_def, name='visual_job_def'),
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
    ### Subcrews
    path('subcrews/', subcrew_def, name='subcrew_def'),
    path('subcrews/subcrew_form/', create_subcrew_form, name='subcrew-form'),
    path('subcrews/<int:pk>/update', update_subcrew, name='update-subcrew'),
    path('subcrews/<int:pk>/detail', detail_subcrew, name='detail-subcrew'),
    path('subcrews/<int:pk>/delete', delete_subcrew, name='delete-subcrew'),
]

