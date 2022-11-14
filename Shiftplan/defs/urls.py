from django.urls import path

from . import views


app_name = 'defs'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.ShiftplanDefView.as_view(), name='shiftplan_def'),
    path('<int:shiftplan_id>/', views.shiftplan_def, name='shiftplan_def'),
    path('<int:shiftplan_id>/time_def/', views.time_def, name='time-def'),
    path('<int:pk>/ti_def/', views.TimeIntervalCreateView.as_view(), name='ti_def'),
    path('<int:pk>/jobtype/', views.jobtype_def, name='jobtype_def'),
    path('<int:pk>/create_jt/', views.create_jobtype, name='create_jobtype'),
    path('htmx/create-jobtype-form/', views.create_jobtype_form, name='create-jobtype-form'),
    path('htmx/jobtype/<pk>/', views.detail_jobtype, name='detail-jobtype'),
    path('htmx/jobtype/<pk>/update/', views.update_jobtype, name='update-jobtype'),
    path('htmx/jobtype/<pk>/delete/', views.delete_jobtype, name='delete-jobtype'),
    path('<int:shiftplan_id>/job_def/', views.job_def, name='job_def'),
]
