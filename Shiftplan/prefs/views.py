import json
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q


import pandas as pd

from defs.models import Shiftplan, Jobtype, Job
from .models import UserJobRating
from .theplot import *

# my_filter_qs = Q()
# for creator in creator_list:
#     my_filter_qs = my_filter_qs | Q(creator=creator)
# my_model.objects.filter(my_filter_qs)


class IndexView(generic.ListView):
    template_name = 'prefs/index.html'
    context_object_name = 'shiftplan_list'

    def get_queryset(self):
        """Return all available shiftplan instances."""
        return Shiftplan.objects.all()


def regain_integrity(shiftplan_id, user):
    # jobtypes = Jobtype.objects.filter(shiftplan_id=shiftplan_id)#.values_list('id', flat=True)
    # jt_jobs = [Job.objects.filter(jobtype_id=jt.id) for jt in jobtypes]
    # l = []
    # for jt, j_qs in zip(jobtypes, jt_jobs):
    #     for j in j_qs:
    jobs = Job.objects.all()
    for j in jobs:
        ujr = UserJobRating.objects.filter(user=user, job=j)
        print(ujr)
        if len(ujr) == 0:
            n_ujr = UserJobRating(user=user, job=j, rating=j.rating)
            n_ujr.save()
    print("REGAIN INTEGRITY: ", jobs)
            
@login_required
def chart_view(request, pk, **kwargs):
    # request.session.flush()
    
    current_user = request.user if type(request.user) is not AnonymousUser else None
    regain_integrity(pk, current_user)
    # print("chart_view: ", UserJobRating.objects.filter(user=current_user))
    user_ratings = UserJobRating.objects.filter(user=current_user)
    l = []
    for ur in user_ratings:
        d = ur.as_dict()
        job = ur.job.as_dict()
        job["db_idx"] = ur.job.id
        jobtype = ur.job.jobtype.as_dict()
        d.update(job)
        d.update(jobtype)
        l.append(d)
    # shiftplan = get_object_or_404(Shiftplan, pk=pk)
    # jobtypes = Jobtype.objects.filter(shiftplan_id=pk)#.values_list('id', flat=True)
    # jt_jobs = [Job.objects.filter(jobtype_id=jt.id) for jt in jobtypes]
    # l = []
    # for jt, j_qs in zip(jobtypes, jt_jobs):
    #     for j in j_qs:
    #         d = jt.as_dict()
    #         j_dict = j.as_dict()
    #         j_dict["db_idx"] = j.id
    #         d.update(j_dict)
    #         l.append(d)
    df = pd.DataFrame(l)
    print(50*'+')
    print(df)
    # df.index = [j.id for j in Job.objects.all()]
    # df.reset_index()
    df['begin'] = pd.to_datetime(df['begin'], format="%Y-%m-%d %H:%M:%S")
    df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d %H:%M:%S")
    # df['during'] = df.end - df.begin
    
    # df['user_id'] = current_user.id
    try:
        print(df['rating'])
    except:
        df['rating'] = 3
    # try:
    #     user_job_rating = UserJobRating.objects.filter(user=current_user)
    #     print("user_job_rating ", user_job_rating)
    # except UserJobRating.DoesNotExist:
    #     user_job_rating = []
    # if len(user_job_rating) == 0:
    #     for jt in jt_jobs:
    #         for j in jt:
    #             ujr = UserJobRating(user=current_user, job=j, rating=j.rating)
    #             ujr.save()
    
    # df = pd.DataFrame([
    #     dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28', Resource="Alex"),
    #     dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15', Resource="Alex"),
    #     dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30', Resource="Max")
    #     ])
    # print(df)
    # set_df(df)
    df = df.to_json()
    session = request.session
    djaploda = session.get('django_dash', {})
    ndf = djaploda.get('df', df)
    ndf = df
    djaploda['df'] = ndf
    session['django_dash'] = djaploda

    # Use some of the information during template rendering
    context = {}
    print(5*'---\n')
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

    # return render(request, 'prefs/chart.html', context)
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
    