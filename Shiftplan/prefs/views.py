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
        # print(ujr)
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
    # df_transactions['date'] = pd.to_datetime(df_transactions['date'])
    # df_transactions['date'] = pd.to_datetime(df_transactions['date'].dt.strftime(format='%d-%m-%Y'))
    # df['begin_date'] = pd.to_datetime(df['begin_date'], format="%Y-%m-%d")
    # df['end_date'] = pd.to_datetime(df['end'], format="%Y-%m-%d")
    # df['begin_time'] = pd.to_datetime(df['begin_date'], format=" %H:%M:%S")
    # df['end_time'] = pd.to_datetime(df['end_date'], format=" %H:%M:%S")
    df['begin'] = pd.to_datetime(df['begin_date'].astype(str) + ' ' + df['begin_time'].astype(str))
    df['end'] = pd.to_datetime(df['end_date'].astype(str) + ' ' + df['end_time'].astype(str))
    # df['during'] = df.end - df.begin
    
    # df['user_id'] = current_user.id
    try:
        print(df['rating'])
    except:
        df['rating'] = 3
    print("CONVERT TO JSON")
    df['begin'] = df['begin'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['end'] = df['end'].dt.strftime('%Y-%m-%d %H:%M:%S')
    context = {"jt_descriptions": [{"name": n, "description": d} for n, d in zip(df['name'], df['description'])]
        # df.loc[df.index==i]["name"]: df.loc[df.index==i]["description"] for i in df.index
    }
    df = df.to_json()
    print(context)
    session = request.session
    djaploda = session.get('django_dash', {})
    ndf = djaploda.get('df', df)
    ndf = df
    djaploda['df'] = ndf
    session['django_dash'] = djaploda    
    print(5*'---\n')
    return render(request, 'prefs/chart.html', context)
