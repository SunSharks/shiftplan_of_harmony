from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed

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
from defs.models import UserProfile, Jobtype, Job
from prefs.models import UserJobRating, BiasHours, UserOptions

from .solplot import *

from utils import config 

time_format = '%Y-%m-%d-%H-%M'
final_solution_path = join("sols", "_json", "solution.json")
final_solution_admin_path = join("sols", "_json", "_admin")


@login_required
def index_view(request):
    final_sol = get_final_final_solution()
    try:
        prepare_session_var(request, final_sol.pk)
    except AttributeError:
        pass
    current_user = request.user
    if current_user.is_superuser:
        return admin_index_view(request, final_sol)
    else:
        return normal_index_view(request, final_sol)


@login_required
def normal_index_view(request, final_sol):
    # TODO
    context = {}
    if type(final_sol) != str:
        context.update({
                "final_sol": final_sol,
                "show_solution": final_sol,
                "show_solution_run": final_sol.solution_run
            })
    else:
        context.update({
            "error_message": final_sol
        })
    return render(request, 'sols/normal_index.html', context)
        


@login_required
def admin_index_view(request, final_sol):
    current_user = request.user
    if current_user.is_superuser:
        context = update_run()
        if type(final_sol) != str:
            context.update({
                "final_sol": final_sol,
                "show_solution": final_sol,
                "show_solution_run": final_sol.solution_run
            })
        else:
            context.update({
                "error_message": final_sol
            })
        return render(request, 'sols/admin_index.html', context)
    else:
        return HttpResponseNotAllowed("You are not superuser.")
    # final_solution = Solution.objects.filter(final=True)
    # print(final_solution)
    # if exists(final_solution_admin_path):
    #     return render(request, 'sols/index.html', context)
    
    # return HttpResponse("Admin index.")


@login_required
def sol_runs_view(request):
    context = update_run()
    sol_runs = SolutionRun.objects.all().order_by('-timestamp')
    final_sol_run = SolutionRun.objects.filter(final=True)
    if len(final_sol_run) == 0:
        context.update({
            "error_message": "No final solrun."
        })
    else:
        context.update({
            "final_sol_run": final_sol_run[0]
        })
    context.update({
                "sol_runs": sol_runs
            })
    return render(request, 'sols/sol_runs.html', context)


@login_required
def admin_solutions_view(request, pk):
    sol_run = get_object_or_404(SolutionRun, id=pk)
    current_user = request.user
    if current_user.is_superuser:
        context = update_run()
    else:
        return HttpResponseNotAllowed("You are not superuser.")
    context.update({
        "solutions": sol_run.solution_set.all()
    })
    return render(request, 'sols/admin_new_sols.html', context)


@login_required
def prepare_session_var(request, pk):
    current_user = request.user
    solution = get_object_or_404(Solution, id=pk) 
    jobs = Job.objects.all()
    if len(jobs) == 0:
        return HttpResponse('<h1>No Jobs defined.</h1>')
    user_job_assignments = UserJobAssignment.objects.all()
    l = []
    for j in jobs:
        user_job_assignments = UserJobAssignment.objects.filter(job=j, assigned=True, solution=solution)
        # print(user_job_assignments)
        if len(user_job_assignments) == 0:
            assigned_username = config.dummy_username
            assigned_rating = 0
            d = {}
        # elif len(user_job_assignments) > 1:
        #     return HttpResponse("Multiple persons assigned to the same job.")
        else:
            assigned_username = user_job_assignments[0].user.username
            assigned_rating = UserJobRating.objects.get(job=user_job_assignments[0].job, user=user_job_assignments[0].user).rating
            
            ura = user_job_assignments[0]
            d = ura.as_dict()
        job = j.as_dict()
        jobtype = j.jobtype.as_dict()
        user_rating = UserJobRating.objects.get(user=current_user, job=j).rating
        d.update({
            "assigned_username": assigned_username
            })
        d.update({
            "assigned_rating": assigned_rating,
            "assigned_rating_str": str(assigned_rating)
        })
        d.update({
            "user_rating": user_rating,
            "user_rating_str": str(user_rating)
        })
        d.update(job)
        popularity = sum([ujr.rating for ujr in UserJobRating.objects.filter(job=j)]) / len(UserJobRating.objects.filter(job=j))
        d.update({
            "popularity": popularity,
            "popularity_str": str(popularity)
        })
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
    djaploda['username'] = current_user.username
    djaploda['is_admin'] = current_user.is_superuser
    session['django_dash'] = djaploda


@login_required
def show_solution_view(request, pk):
    solution = get_object_or_404(Solution, id=pk)  
    jobs = Job.objects.all()
    if len(jobs) == 0:
        return HttpResponse('<h1>No Jobs defined.</h1>')
    # print(5*'---\n')
    prepare_session_var(request, pk)
    context = {
        "show_solution": solution,
        "show_solution_run": solution.solution_run
    }
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'sols/admin_show_sol.html', context)
    else:
        return render(request, 'sols/normal_show_sol.html', context)


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
def set_sol_run_final_view(request, pk):
    solution_run = get_object_or_404(SolutionRun, id=pk)
    solution_run.final = True
    solution_run.save()
    return redirect("sols:index")


@login_required
def unset_sol_run_final_view(request):
    context = update_run()
    final_sol_run = SolutionRun.objects.filter(final=True)
    if len(final_sol_run) != 0:
        final_sol_run[0].final = False 
        final_sol_run[0].save()
    return redirect("sols:sol_runs")


@login_required
def set_sol_final_view(request, pk):
    solution = get_object_or_404(Solution, id=pk)
    solution.final = True
    solution.save()
    return redirect("sols:index")
    # admin_new_solutions_view(request, pk=pk, set_final=True)
    # return HttpResponse("")
    # return redirect("sols:show_solution", pk=pk, set_final=True)


@login_required
def unset_sol_final_view(request, pk):
    context = update_run()
    solution_run = get_object_or_404(SolutionRun, id=pk)
    final_sol = Solution.objects.filter(solution_run=solution_run, final=True)
    if len(final_sol) != 0:
        final_sol[0].final = False 
        final_sol[0].save()
    return redirect("sols:sol_runs")


@login_required
def stats_view(request, pk):
    solution = get_object_or_404(Solution, id=pk)
    prepare_session_var(request, pk)
    session = request.session
    djaploda = session.get('django_dash', {})
    df = pd.read_json(djaploda.get('df', {}))
    df['begin'] = pd.to_datetime(df['begin'], format="%Y-%m-%d %H:%M:%S")
    df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d %H:%M:%S")
    df['during'] = df['end'] - df['begin']
    print(df)
    current_user = request.user
    num_workers = len(UserProfile.objects.filter(worker=True))
    num_jobs = len(Job.objects.all())
    sum_working_hours = df["during"].sum()
    sum_bias_hours = sum([b.bias_hours for b in BiasHours.objects.all()])
    sum_working_hours += pd.to_timedelta(sum_bias_hours, unit='h')
    avg_workload = sum_working_hours / num_workers

    user_assigned_jobs = UserJobAssignment.objects.filter(solution=solution, user=current_user, assigned=True)
    user_num_jobs = len(user_assigned_jobs)
    print(df.loc[df["user"] == current_user.pk])
    df_user_assigned = df.loc[df["user"] == current_user.pk]
    user_workload = df_user_assigned["during"].sum()
    user_break = UserOptions.objects.filter(user=current_user)[0].min_break_hours
    user_break_str = f"{user_break} hours between 2 shifts"
    workloads_per_person = df.groupby(['user'])["during"].sum()
    max_workload = workloads_per_person.max()
    min_workload = workloads_per_person.min()
    print(max_workload)
    stats = [
        {"label": t[0], "value": t[1], "title": t[2]} for t in [
            ("User", current_user.username, ""),
            ("My break", user_break_str, ""),
            ("Workers", num_workers, ""),
            ("Jobs", num_jobs, ""),
            ("My Jobs", user_num_jobs, ""),
            ("Total Workload", sum_working_hours, ""),
            ("Average Workload", avg_workload, ""),
            ("My Workload", user_workload, ""),
            ("Max Workload", max_workload, ""),
            ("Min Workload", min_workload, "")
        ]
    ]
    context = {}
    context.update({
        "stats": stats
    })
    return render(request, 'sols/stats.html', context)


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


def set_final_solution(pk):
    solution = get_object_or_404(Solution, id=pk)
    solution.final = True
    solution.save()


def update_run():
    latest_sol_run = SolutionRun.objects.all().order_by('-timestamp').first()
    files_timestamps = [datetime.strptime(fn.replace(".json", ""), time_format) for fn in listdir(final_solution_admin_path)]
    if len(files_timestamps) > 0:
        latest_admin_json_dt = max(files_timestamps)
        if not latest_sol_run is None:
            latest_sol_run_dt = datetime.strptime(datetime.strftime(latest_sol_run.timestamp, time_format), time_format)
            if latest_admin_json_dt > latest_sol_run_dt:
                new_run(latest_admin_json_dt)
                context = {
                    'admin_new_solution': True,
                    'existing_solutions': True
                }
            else:
                context = {
                    'admin_new_solution': False,
                    'existing_solutions': True
                }
        else:
            new_run(latest_admin_json_dt)
            context = {
                    'admin_new_solution': True,
                    'existing_solutions': True
                }
    else:
        context = {
            'admin_new_solution': False,
            'existing_solutions': False
        }
    return context


def get_latest_run():
    latest_sol_run = SolutionRun.objects.all().order_by('-timestamp').first()
    context.update({
        "solutions": latest_sol_run.solution_set.all()
    })


def get_final(model, **kwargs):
    final = model.objects.filter(final=True, **kwargs)
    if len(final) == 1:
        return final[0]
    elif len(final) == 0: 
        return 0
    else:
        return "More than 1 final. "


def get_final_final_solution():
    final_sol_run = get_final(SolutionRun)
    if final_sol_run == 0:
        return "No final SolutionRun defined."
    elif type(final_sol_run) == str:
        return "More than 1 final SolutionRuns."
    else:
        final_sol = get_final(Solution, solution_run=final_sol_run)
        if final_sol == 0:
            return "No final Solution defined."
        elif type(final_sol) == str:
            return "More than 1 final Solutions."
        else:
            return final_sol
    # print("final_sol_run", final_sol_run)
    # latest_sol_run = SolutionRun.objects.all().order_by('-timestamp').first()
    # context.update({
    #     "solutions": latest_sol_run.solution_set.all()
    # })