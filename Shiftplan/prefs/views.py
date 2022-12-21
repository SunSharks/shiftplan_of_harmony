import json
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import pandas as pd

from defs.models import Shiftplan, Jobtype, Job
from .models import UserJobRating
from .theplot import *


class IndexView(generic.ListView):
    template_name = 'prefs/index.html'
    context_object_name = 'shiftplan_list'

    def get_queryset(self):
        """Return all available shiftplan instances."""
        return Shiftplan.objects.all()

@login_required
def chart_view(request, pk, **kwargs):
    current_user = request.user
    # print(current_user.id)
    shiftplan = get_object_or_404(Shiftplan, pk=pk)
    jobtypes = Jobtype.objects.filter(shiftplan_id=pk)#.values_list('id', flat=True)
    # print(jobtypes)
    jt_jobs = [Job.objects.filter(jobtype_id=jt.id) for jt in jobtypes]
    # print(jt_jobs)
    l = []
    for jt, j_qs in zip(jobtypes, jt_jobs):
        for j in j_qs:
            d = jt.as_dict()
            d.update(j.as_dict())
            l.append(d)
    df = pd.DataFrame(l)
    # print(l)
    # print(df)
    df['begin'] = pd.to_datetime(df['begin'], format="%Y-%m-%d %H:%M:%S")
    df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d %H:%M:%S")
    # df['during'] = df.end - df.begin
    
    df['user_id'] = current_user.id
    try:
        print(df['rating'])
    except:
        df['rating'] = 3
    user_job_rating = UserJobRating.objects.filter(user=current_user)
    if len(user_job_rating) == 0:
        for jt in jt_jobs:
            for j in jt:
                ujr = UserJobRating(user=current_user, job=j, rating=j.rating)
                ujr.save()
    
    # df = pd.DataFrame([
    #     dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28', Resource="Alex"),
    #     dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15', Resource="Alex"),
    #     dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30', Resource="Max")
    #     ])
    # print(df)
    # set_df(df)
    context = {}
    dash_context = request.session.get("django_dash")
    # print(dash_context)
    dash_context['df'] = df.to_json()
    request.session['django_dash'] = dash_context
    return render(request, 'prefs/chart.html', context)

# class Tst:
#     def __init__(self):
#         self.Task = "Job A"
#         self.Start = '2009-01-01'
#         self.Finish = '2009-02-01'
#         self.Resource = "Alex"

#     def as_dict(self):
#         return {'Task': self.Task, 'Start': self.Start, 'Finish': self.Finish, 'Resource': self.Resource}


# tst = [Tst()]
# df = pd.DataFrame([x.as_dict() for x in tst])

    return render(request, 'prefs/chart.html', context)
    # answers = Answer.objects.filter(question_id=1).select_related() 
    # qs = Chart.objects.all()
    # projects_data = [
    #     {
    #         'Project': x.name,
    #         'Start': x.start_date,
    #         'Finish': x.finish_date,
    #         'Responsible': x.responsible.username
    #     } for x in qs
    # ]
    # df = pd.DataFrame(projects_data)
    # fig = px.timeline(
    #     df, x_start="Start", x_end="Finish", y="Project", color="Responsible"
    # )
    # 
    