import logging
import pandas as pd
from datetime import datetime, timedelta
import json
# from os import listdir
# from os.path import exists, join

from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed

from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

from django.conf import settings
from django.utils.timezone import make_aware
from django.utils.datastructures import MultiValueDictKeyError

from utils.create_instances import *
from utils import config

from .admin_prefplot import *
from defs.models import Shiftplan, UserProfile, Jobtype, Job
from prefs.models import UserJobRating, BiasHours, UserOptions, Workload


@login_required
def admin_prefs_view(request):
    context = {}
    current_user = request.user
    if current_user.is_superuser:
        context = {}
    else:
        return HttpResponseNotAllowed("You are not superuser.")
        
    try:    
        selected_user = request.GET['users']
        selected_user = User.objects.get(pk=selected_user)
        selected_user_pk = selected_user.pk
        logging.debug(selected_user.username)
    except MultiValueDictKeyError:
        selected_user_pk = None
        
    

    worker_insts = UserProfile.objects.filter(worker=True)
    workers = []
    for w in worker_insts:
        w_user = w.user
        pk = w.user.pk
        username = w.user.username
        workers.append({'label': username, 'value': pk, 'selected': pk == selected_user_pk})
    workers = sorted(workers, key=lambda d: d['label'])
    if selected_user_pk is None:
        selected_user = User.objects.get(pk=workers[0]["value"])
    jobtypes = Jobtype.objects.all()
    if len(jobtypes) == 0:
        return HttpResponse('<h1>No Jobtypes defined.</h1>') 
    jobs_allowed = []
    for jt in jobtypes:
        if jt.subcrew:
            if not selected_user in jt.subcrew.members.all():
                continue
        # print(jt.job_set.all().values_list("pk", flat=True))
        jobs_allowed.extend(jt.job_set.all())
    if len(jobs_allowed) == 0:
        return HttpResponse('<h1>No Jobs defined.</h1>') 
    ok_job_qs = Q()
    for job_pk in jobs_allowed:
        ok_job_qs = ok_job_qs | Q(job=job_pk, user=selected_user)
    user_ratings = UserJobRating.objects.filter(ok_job_qs)
    # print(50*'+')
    # print(user_ratings)
    l = []
    for ur in user_ratings:
        d = ur.as_dict()
        job = ur.job.as_dict()
        job["db_idx"] = ur.job.id
        jobtype = ur.job.jobtype.as_dict()
        d.update(job)
        d.update(jobtype)
        l.append(d)

    df = pd.DataFrame(l)
 
    df['begin'] = pd.to_datetime(df['begin_date'].astype(str) + ' ' + df['begin_time'].astype(str))
    df['end'] = pd.to_datetime(df['end_date'].astype(str) + ' ' + df['end_time'].astype(str))
    # df['during'] = df.end - df.begin
    
    # logging.debug(df["rating"])
    # print("CONVERT TO JSON")
    df['begin'] = df['begin'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['end'] = df['end'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df = df.to_json()
    # print(context)
    session = request.session
    djaploda = session.get('django_dash', {})
    ndf = djaploda.get('df', df)
    ndf = df
    djaploda['df'] = ndf
    session['django_dash'] = djaploda  

    context.update({
        "workers": workers,
        "selected_user": selected_user.pk
    })
    return render(request, 'admin_prefs/main_admin_pref.html', context)