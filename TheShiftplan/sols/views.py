import logging
import pandas as pd
from datetime import datetime, timedelta
import json
from os import listdir
from os.path import exists, join

from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed

from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

from django.conf import settings
from django.utils.timezone import make_aware

from utils.create_instances import *
from utils import config

from .solplot import *
from .models import SolutionRun, Solution, UserJobAssignment
from defs.models import UserProfile, Jobtype, Job
from prefs.models import UserJobRating, BiasHours, UserOptions


time_format = '%Y-%m-%d-%H-%M'
final_solution_path = join("sols", "_json", "solution.json")
final_solution_admin_path = join("sols", "_json", "_admin")


def test():
    # sol_runs = SolutionRun.objects.all()
    logging.debug(Jobtype.objects.filter(default_rating=5))
    logging.debug(Jobtype.objects.filter(default_rating=3))
    # logging.debug(Jobtype.objects.get(default_rating=3))
    fin_sol_run = SolutionRun.objects.get(final=True)
    logging.debug(SolutionRun.objects.get(final=True))
    # logging.debug(Job.objects.get)
    logging.debug(Solution.objects.filter(solution_run=fin_sol_run, final=True))


@login_required
def index_view(request):
    # test()
    final_sol = get_final_distribution()
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
        context = update_run(request)
        logging.debug(context["admin_new_solution"])
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
    context = update_run(request)
    sol_runs = SolutionRun.objects.all().order_by('-timestamp')
    final_sol_run = SolutionRun.objects.filter(final=True)
    session = request.session
    new_runs_pks = session.get("new_runs_pks", [])
    if len(final_sol_run) == 0:
        context.update({
            "error_message": "No final solrun."
        })
    else:
        context.update({
            "final_sol_run": final_sol_run[0]
        })
    context.update({
        "sol_runs": sol_runs,
        "new_runs_pks": new_runs_pks
    })
    return render(request, 'sols/sol_runs.html', context)


@login_required
def admin_solutions_view(request, pk):
    sol_run = get_object_or_404(SolutionRun, id=pk)
    current_user = request.user
    if current_user.is_superuser:
        context = update_run(request)
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
            try:
                dummy_user = User.objects.get(username=config.dummy_username)
            except User.DoesNotExist:
                dummy_user = User(username=config.dummy_username)
                dummy_user.save()
                dummy_profile = UserProfile.objects.get(user=dummy_user)
                setattr(dummy_profile, "worker", False)
                dummy_profile.save()
            assigned_username = config.dummy_username
            assigned_rating = 0
            d = {
                "job": j.pk,
                "user": dummy_user.pk
            }
        elif len(user_job_assignments) > 1:
            logging.warning("Multiple persons assigned to the same job.")
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
            "assigned_rating": str(assigned_rating)
        })
        d.update({
            "user_rating": str(user_rating)
        })
        d.update(job)
        popularity = sum([ujr.rating for ujr in UserJobRating.objects.filter(job=j)]) / len(UserJobRating.objects.filter(job=j))
        d.update({
            "popularity": popularity,
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
    return df


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


# def get_or_create(model, **kwargs):
#     try:
#         instance = model.objects.get(**kwargs)
#         # print("existing {}: {}".format(model, instance))
#     except model.DoesNotExist:
#         instance = model(**kwargs)
#         instance.save()
#         # print("new {}: {}".format(model, instance))
#     # user_options = UserOptions.objects.get(user=current_user)
#     return instance

#     context = {
#     }
#     return render(request, 'sols/show_sol.html', context)


@login_required
def set_sol_run_final_view(request, pk):
    solution_run = get_object_or_404(SolutionRun, id=pk)
    solution_run.final = True
    solution_run.save()
    return redirect("sols:index")


@login_required
def unset_sol_run_final_view(request):
    context = update_run(request)
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
    context = update_run(request)
    solution_run = get_object_or_404(SolutionRun, id=pk)
    final_sol = Solution.objects.filter(solution_run=solution_run, final=True)
    if len(final_sol) != 0:
        final_sol[0].final = False 
        final_sol[0].save()
    return redirect("sols:sol_runs")


# def get_workload(user_profiles)


@login_required
def workload_list_view(request, pk):
    solution = get_object_or_404(Solution, id=pk)
    prepare_session_var(request, pk)
    session = request.session
    djaploda = session.get('django_dash', {})
    df = pd.read_json(djaploda.get('df', {}))
    df['begin'] = pd.to_datetime(df['begin'], format="%Y-%m-%d %H:%M:%S")
    df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d %H:%M:%S")
    df['during'] = df['end'] - df['begin']
    # logging.debug(df.columns)
    worker_insts = UserProfile.objects.filter(worker=True)
    workers = []
    for w in worker_insts:
        w_user = w.user
        df_user_assigned = df.loc[df["user"] == w_user.pk]
        user_workload = df_user_assigned["during"].sum()
        username = w.user.username
        bias = BiasHours.objects.get(user=w.user).bias_hours
        # logging.debug(bias)
        # logging.debug(df_user_assigned)
        # logging.debug()
        workers.append({
            "username": username,
            "workload": user_workload    
        })
    non_worker_insts = UserProfile.objects.filter(worker=False)
    non_workers = []
    for w in non_worker_insts:
        username = w.user.username
        w_user = w.user
        df_user_assigned = df.loc[df["user"] == w_user.pk]
        user_workload = df_user_assigned["during"].sum()
        non_workers.append({
            "username": username,
            "workload": user_workload    
        })
    if len(non_workers) != 0:
        context = {
            "workers": workers,
            "non_workers": non_workers
        }
    else:
        context = {
            "workers": workers
        }
    return render(request, 'sols/workload_list.html', context)


@login_required
def stats_view(request, pk):
    solution = get_object_or_404(Solution, id=pk)
    df = prepare_session_var(request, pk)
    df = pd.read_json(df)
    # session = request.session
    # djaploda = session.get('django_dash', {})
    # df = pd.read_json(djaploda.get('df', {}))
    # logging.debug(df)
    df['begin'] = pd.to_datetime(df['begin'], format="%Y-%m-%d %H:%M:%S")
    df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d %H:%M:%S")
    df['during'] = df['end'] - df['begin']
    # logging.debug(df)
    current_user = request.user
    num_workers = len(UserProfile.objects.filter(worker=True))
    num_jobs = len(Job.objects.all())
    sum_working_hours = df["during"].sum()
    sum_bias_hours = sum([b.bias_hours for b in BiasHours.objects.all()])
    sum_working_hours += pd.to_timedelta(sum_bias_hours, unit='h')
    avg_workload = sum_working_hours / num_workers

    # user_assigned_jobs = UserJobAssignment.objects.filter(solution=solution, user=current_user, assigned=True)
    # print(df.loc[df["user"] == current_user.pk])
    df_user_assigned = df.loc[df["user"] == current_user.pk]
    user_num_jobs = len(df_user_assigned.index)
    user_workload = df_user_assigned["during"].sum()
    user_break = UserOptions.objects.filter(user=current_user)[0].min_break_hours
    user_break_str = f"{user_break} hours between 2 shifts"
    workloads_per_person = df.groupby(['user'])["during"].sum()
    max_workload = workloads_per_person.max()
    min_workload = workloads_per_person.min()
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
    if current_user.is_superuser:

        context.update({
            "is_admin": True
        })
    return render(request, 'sols/stats.html', context)


def create_objects(request, objs, dt):
    # logging.debug(type(dt))
    # logging.debug(dt)
    # logging.debug(SolutionRun.objects.filter(timestamp=dt))
    # logging.debug(SolutionRun.objects.all().order_by('-timestamp').first())
    # for sr in SolutionRun.objects.all():
    #     sr.timestamp = make_aware(sr.timestamp)
    #     sr.save()
    #     logging.info(sr.timestamp.tzinfo)
    #     logging.debug(sr)
    try:
        sol_run = SolutionRun(timestamp=dt)
        sol_run.save()
        logging.info("New SolutionRun object.")
        session = request.session
        # new_runs = session.get("new_runs", [])
        # new_runs.append(sol_run.as_dict())
        # session["new_runs"] = new_runs
        new_runs_pks = session.get("new_runs_pks", [])
        new_runs_pks.append(sol_run.pk)
        session["new_runs_pks"] = new_runs_pks
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
    

def new_run(request, latest_admin_json_dt):
    admin_json_file = join(final_solution_admin_path, datetime.strftime(latest_admin_json_dt, time_format) + ".json")
    with open(admin_json_file, 'r') as f:
        objs = json.load(f)
    time_offset = timedelta(hours=settings.TIME_OFFSET)
    create_objects(request, objs, latest_admin_json_dt + time_offset)


def set_final_solution(pk):
    solution = get_object_or_404(Solution, id=pk)
    solution.final = True
    solution.save()


def update_run(request):
    latest_sol_run = SolutionRun.objects.all().order_by('-timestamp').first()
    # logging.debug(latest_sol_run)
    files_timestamps = [datetime.strptime(fn.replace(".json", ""), time_format) for fn in listdir(final_solution_admin_path)]
    if len(files_timestamps) > 0:
        latest_admin_json_dt = max(files_timestamps)
        logging.debug(latest_admin_json_dt)
        if not latest_sol_run is None:
            logging.debug(latest_sol_run.timestamp)
            latest_sol_run_dt = datetime.strptime(datetime.strftime(latest_sol_run.timestamp, time_format), time_format)
            latest_sol_run_dt = latest_sol_run.timestamp
            # latest_sol_run_dt = make_aware(latest_sol_run_dt)
            time_offset = timedelta(hours=settings.TIME_OFFSET)
            # latest_admin_json_dt = latest_admin_json_dt + time_offset
            latest_admin_json_dt = make_aware(latest_admin_json_dt)
            # logging.debug(latest_admin_json_dt)
            if latest_admin_json_dt + time_offset > latest_sol_run_dt:
                logging.debug("latest_admin_json_dt > latest_sol_run_dt")
                logging.debug(f"{latest_admin_json_dt} > {latest_sol_run_dt}")
                new_run(request, latest_admin_json_dt)
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
            new_run(request, latest_admin_json_dt)
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


def get_final_distribution():
    final_sol_run = get_final(SolutionRun)
    if final_sol_run == 0:
        return "No final SolutionRun defined."
    elif type(final_sol_run) == str:
        return "More than 1 final SolutionRuns."
    else:
        final_sol = get_final(Solution, solution_run=final_sol_run)
        # logging.debug(final_sol)
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


class Shift:

    NONE_STR = "None"

    def __init__(self, id, shift_name, username, begin, end, has_predecessors=True, has_successors=False):
        self.has_predecessors = has_predecessors
        self.has_successors = has_successors
        self.id = id
        self.name = shift_name
        self.username = username
        self.begin = begin
        self.end = end
        self.during = end - begin

        self.get_strings()


    def get_strings(self):
        self.begin_dayname = self.begin.day_name()
        self.end_dayname = self.end.day_name()
        self.begin_str = self.begin.strftime("%Y-%m-%d %H:%M")
        self.end_str = self.end.strftime("%Y-%m-%d %H:%M")
        self.begin_date_str = self.begin.date().strftime("%Y-%m-%d")
        self.end_date_str = self.end.date().strftime("%Y-%m-%d")
        self.begin_time_str = self.begin.time().strftime("%H:%M")
        self.end_time_str = self.end.time().strftime("%H:%M")

        during_hrs = self.during.seconds / 3600
        int_during_hrs = self.during.seconds // 3600
        if during_hrs == int_during_hrs:
            self.during_str = f"{int_during_hrs} h"
        else:
            during_minutes = (during_hrs - int_during_hrs) * 60
            self.during_str = f"{int_during_hrs} h {during_minutes} m"


class Predecessor(Shift):
    def __init__(self, parent_id, shift_name, username, begin, end):
        self.parent_id = parent_id
        super().__init__(None, shift_name, username, begin, end)

class Successor(Shift):
    def __init__(self, parent_id, shift_name, username, begin, end):
        self.parent_id = parent_id
        super().__init__(None, shift_name, username, begin, end)


def get_predecessors(df, user_df):
    """
    Returns (list[<shift_instances>], list[<predecessor_instances>])
    with shift_instances containing shift objects of own shifts and
    predecessor_instances containing corresponding predecessor objects.
    @param df: Whole DataFrame containing predecessor candidates.
    @param user_df: Filtered DataFrame containing only data from which a shift object is to be created.
    """
    pre_insts = []
    suc_insts = []
    shift_insts = []
    for i in user_df.index:
        pre = df.loc[(df["end"] == user_df["begin"][i]) & (df["name"] == user_df["name"][i])]
        suc = df.loc[(df["begin"] == user_df["end"][i]) & (df["name"] == user_df["name"][i])]
        has_predecessors = bool(len(pre.index))
        has_successors = bool(len(suc.index))
        new_shift = Shift(i, user_df["name"][i], user_df["assigned_username"][i], user_df["begin"][i], user_df["end"][i], has_predecessors, has_successors)
        shift_insts.append(new_shift)
        for j in pre.index:
            pre_inst = Predecessor(i, pre["name"][j], pre["assigned_username"][j], pre["begin"][j], pre["end"][j])
            pre_insts.append(pre_inst)
        for j in suc.index:
            suc_inst = Successor(i, suc["name"][j], suc["assigned_username"][j], suc["begin"][j], suc["end"][j])
            suc_insts.append(suc_inst)
    return shift_insts, pre_insts, suc_insts


# def to_dt(df):
#     df['begin'] = pd.to_datetime(df['begin'], format="%Y-%m-%d %H:%M:%S")
#     df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d %H:%M:%S")
#     df['begin_date'] = pd.to_datetime(df['begin_date'], format="%Y-%m-%d")
#     df['end_date'] = pd.to_datetime(df['end_date'], format="%Y-%m-%d")
#     df['begin_time'] = pd.to_datetime(df['begin_time'], format="%H:%M:%S")
#     df['end_time'] = pd.to_datetime(df['end_time'], format="%H:%M:%S")
#     return df 


# def dt_to_str(df):
#     df['begin_str'] = df['begin'].dt.strftime("%Y-%m-%d %H:%M:%S")
#     df['end_str'] = df['end'].dt.strftime("%Y-%m-%d %H:%M:%S")
#     df['begin_date_str'] = df['begin_date'].dt.strftime("%Y-%m-%d")
#     df['end_date_str'] = df['end_date'].dt.strftime("%Y-%m-%d")
#     df['begin_time_str'] = df['begin_time'].dt.strftime("%H:%M:%S")
#     df['end_time_str'] = df['end_time'].dt.strftime("%H:%M:%S")
#     return df

@login_required
def own_shifts_view(request):
    current_user = request.user
    final_sol = get_final_distribution()
    df = prepare_session_var(request, final_sol.pk)
    df = pd.read_json(df)
    df['begin'] = pd.to_datetime(df['begin'], format="%Y-%m-%d %H:%M:%S")
    df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d %H:%M:%S")
    df["index_col"] = df.index
    user_df = df.loc[df["user"] == current_user.pk].sort_values(["name", "begin"])
    
    # logging.debug(user_df)
    # print(df.columns)
    shift_insts, predecessors, successors = get_predecessors(df, user_df)
    user_df['begin'] = user_df['begin'].dt.strftime("%Y-%m-%d %H:%M:%S")
    user_df['end'] = user_df['end'].dt.strftime("%Y-%m-%d %H:%M:%S")
    user_df = user_df.to_dict('records')
    # logging.debug(user_df)
    context = {
        "shifts": shift_insts,
        "predecessors": predecessors,
        "successors": successors
        }
    return render(request, 'sols/own_shifts.html', context)