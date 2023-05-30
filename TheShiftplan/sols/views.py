from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

import pandas as pd

from datetime import datetime
import json
from os import listdir
from os.path import exists, join

from utils.create_instances import *

from .models import SolutionRun, Solution, UserJobAssignment
from defs.models import Jobtype, Job
from prefs.models import UserJobRating

from .solplot import *

from utils import config 

time_format = '%Y-%m-%d-%H-%M'
final_solution_path = join("sols", "_json", "solution.json")
final_solution_admin_path = join("sols", "_json", "_admin")

@login_required
def index_view(request):
    current_user = request.user
    print(current_user.is_superuser)
    if current_user.is_superuser:
        return admin_index_view(request)
    else:
        return normal_index_view(request)


def create_objects(objs, dt):
    try:
        sol_run = SolutionRun(timestamp=dt)
        sol_run.save()
    except IntegrityError:
        return
    for key, val in objs.items():
        solution = Solution(solution_run=sol_run)
        solution.save()
        for l in val:
            l["user"] = User.objects.get(pk=l["user"])
            l["job"] = Job.objects.get(pk=l["job"])
            instance = UserJobAssignment()
            for k, v in l.items():
                setattr(instance, k, v)
            setattr(instance, "solution", solution)
            instance.save()
    

def new_run(latest_admin_json_dt):
    admin_json_file = join(final_solution_admin_path, datetime.strftime(latest_admin_json_dt, time_format) + ".json")
    with open(admin_json_file, 'r') as f:
        objs = json.load(f)
    create_objects(objs, latest_admin_json_dt)


def set_final_solution(final_solution_pk):
    pass 


@login_required
def admin_index_view(request):
    latest_sol_run = SolutionRun.objects.all().order_by('-timestamp').first()
    
    # print(SolutionRun.objects.all())
    # print(datetime.strptime(datetime.strftime(latest_sol_run.timestamp, time_format), time_format))
    files_timestamps = [datetime.strptime(fn.replace(".json", ""), time_format) for fn in listdir(final_solution_admin_path)]
    if len(files_timestamps) > 0:
        latest_admin_json_dt = max(files_timestamps)
        if not latest_sol_run is None:
            latest_sol_run_dt = datetime.strptime(datetime.strftime(latest_sol_run.timestamp, time_format), time_format)
            if latest_admin_json_dt > latest_sol_run_dt:
                new_run(latest_admin_json_dt)
                context = {
                    'admin_new_solution': True
                }
        else:
            new_run(latest_admin_json_dt)
            context = {
                    'admin_new_solution': True
                }
            return render(request, 'sols/index.html', context)

    if exists(final_solution_admin_path):
        return render(request, 'sols/index.html', context)
    
    return HttpResponse("Admin index.")


@login_required
def admin_new_solutions_view(request):
    latest_sol_run = SolutionRun.objects.all().order_by('-timestamp').first()
    context = {
        "solutions": latest_sol_run.solution_set.all()
    }
    return render(request, 'sols/admin_new_sols.html', context)


@login_required
def show_solution_view(request, pk):
    jobs = Job.objects.all()
    if len(jobs) == 0:
        return HttpResponse('<h1>No Jobs defined.</h1>')
   
    user_job_assignments = UserJobAssignment.objects.all()
    # print(50*'+')
    # print(user_ratings)
    l = []

    for j in jobs:
        user_job_assignments = UserJobAssignment.objects.filter(job=j, assigned=True)
        print(user_job_assignments)
        if len(user_job_assignments) == 0:
            assigned_username = config.dummy_username
            d = {}
        elif len(user_job_assignments) > 1:
            return HttpResponse("Multiple persons assigned to the same job.")
        else:
            assigned_username = user_job_assignments[0].user.username
            ura = user_job_assignments[0]
            d = ura.as_dict()
        job = j.as_dict()
        jobtype = j.jobtype.as_dict()
        d.update({"assigned_username": assigned_username})
        d.update(job)
        popularity = sum([ujr.rating for ujr in UserJobRating.objects.filter(job=j)]) / len(UserJobRating.objects.filter(job=j))
        d.update({"popularity": popularity})
        d.update(jobtype)
        l.append(d)

    df = pd.DataFrame(l)
    df['begin'] = pd.to_datetime(df['begin_date'].astype(str) + ' ' + df['begin_time'].astype(str))
    df['end'] = pd.to_datetime(df['end_date'].astype(str) + ' ' + df['end_time'].astype(str))
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
    # print(5*'---\n')
    context = {
    }
    return render(request, 'sols/show_sol.html', context)

def get_or_create(model, **kwargs):
    try:
        instance = model.objects.get(**kwargs)
        # print("existing {}: {}".format(model, instance))
    except model.DoesNotExist:
        instance = model(**kwargs)
        instance.save()
        # print("new {}: {}".format(model, instance))
    # user_options = UserOptions.objects.get(user=current_user)
    return instance

    context = {
    }
    return render(request, 'sols/show_sol.html', context)


@login_required
def normal_index_view(request):
    # TODO
    if exists(final_solution_path):
        return HttpResponse("Solution exists.")
    return HttpResponse("Solution doesn't exist.")


