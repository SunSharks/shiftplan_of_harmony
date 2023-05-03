import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q




import pandas as pd

from defs.models import Jobtype, Job
from .models import UserJobRating, UserOptions
from .forms import UserOptionsForm
from .theplot import *


def regain_integrity(user):
    jobs = Job.objects.all()
    for j in jobs:
        ujr = UserJobRating.objects.filter(user=user, job=j)
        # print(ujr)
        if len(ujr) == 0:
            n_ujr = UserJobRating(user=user, job=j, rating=j.rating)
            n_ujr.save()
    # print("REGAIN INTEGRITY: ", jobs)
            
@login_required
def chart_view(request, **kwargs):
    # request.session.flush()
    current_user = request.user if type(request.user) is not AnonymousUser else None
    regain_integrity(current_user)
    jobtypes = Jobtype.objects.all()
    jobs_allowed = []
    for jt in jobtypes:
        # print(jt.job_set.all().values_list("pk", flat=True))
        jobs_allowed.extend(jt.job_set.all())
    ok_job_qs = Q()
    for job_pk in jobs_allowed:
        ok_job_qs = ok_job_qs | Q(job=job_pk, user=current_user)
    user_ratings = UserJobRating.objects.filter(ok_job_qs)
    print(50*'+')
    print(user_ratings)
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
    # print(50*'+')
    # print(df)
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
    # print("CONVERT TO JSON")
    df['begin'] = df['begin'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['end'] = df['end'].dt.strftime('%Y-%m-%d %H:%M:%S')
    context = {"jt_descriptions": [{"name": n, "description": d} for n, d in zip(df['name'], df['description'])]
        # df.loc[df.index==i]["name"]: df.loc[df.index==i]["description"] for i in df.index
    }
    print(type(df["user"][0]))
    df = df.to_json()
    # print(context)
    session = request.session
    djaploda = session.get('django_dash', {})
    ndf = djaploda.get('df', df)
    ndf = df
    djaploda['df'] = ndf
    session['django_dash'] = djaploda  
    # print(5*'---\n')
    return render(request, 'prefs/chart.html', context)

def get_or_create_user_options(current_user):
    try:
        user_options = UserOptions.objects.get(user=current_user)
        print("existing user_options: {}".format(user_options))
    except UserOptions.DoesNotExist:
        user_options = UserOptions(user=current_user)
        user_options.save()
        print("new user_options: {}".format(user_options))
    user_options = UserOptions.objects.get(user=current_user)
    return user_options

@login_required
def user_options_view(request):
    current_user = request.user if type(request.user) is not AnonymousUser else None
    user_options = get_or_create_user_options(current_user)
    form = UserOptionsForm(current_user, request.POST or None, instance=user_options)
    if request.method == "POST":
        print("POST")
        if form.is_valid():
            form.save()
            # print("form valid user_options: {}".format(user_options))
            return redirect("prefs:user_options_detail")
            # return render(request, "prefs/user_options_detail.html", context={
            #     "user": current_user,
            #     "min_break_hours": user_options.min_break_hours
            # })
        # else:
    return render(request, "prefs/user_options_form.html", context={
        "form": form,
        "user_options": user_options
    })
    # else:
    #     return render(request, "prefs/user_options.html", context={
    #         "form": form
    #     })
    # return render(request, "prefs/user_options_detail.html", context={
    #             "user": current_user,
    #             "min_break_hours": user_options.min_break_hours
    #         })
    # return render(request, "prefs/user_options.html")
    # if request.method == "POST":
    #     if form.is_valid():
    #         user_options = form.save(commit=False)
    #         # jobtype.shiftplan = shiftplan
    #         user_options.save()
    #         return redirect("prefs:index")
    #     else:
    #         return render(request, "prefs/user_options_form.html", context={
    #             "form": form
    #         })
        # try:
        #     min_break_hours = request.POST['min_break_hours']
        # except KeyError:
        #     # Redisplay the question voting form.
        #     return render(request, 'prefs/user_options.html', {
        #         'user': current_user,
        #         'error_message': "You didn't select a choice.",
        #     })
        # else:
        #     user_options.min_break_hours = min_break_hours
        #     user_options.save()
        #     # Always return an HttpResponseRedirect after successfully dealing
        #     # with POST data. This prevents data from being posted twice if a
        #     # user hits the Back button.
        #     return HttpResponseRedirect(reverse('prefs:user_options'))
    context = {
        'user': current_user,
        'form': form
    }
    return render(request, 'prefs/user_options_form.html', context)

@login_required
def user_options_form(request):
    current_user = request.user if type(request.user) is not AnonymousUser else None
    user_options = get_or_create_user_options()
    form = UserOptionsForm(current_user)
    context = {
        "form": form,
        "user_options": user_options
    }
    return render(request, "prefs/user_options_form.html", context)

@login_required
def user_options_detail(request):
    current_user = request.user if type(request.user) is not AnonymousUser else None
    user_options = get_or_create_user_options(current_user)
    min_break_hours = user_options.min_break_hours
    context = {
        'user': current_user,
        'min_break_hours': min_break_hours
    }
    return render(request, 'prefs/user_options_detail.html', context)

# @login_required
# def create_jobtype(request, pk):
#     shiftplan = get_object_or_404(Shiftplan, pk=pk)
#     jobtypes = Jobtype.objects.filter(shiftplan=shiftplan)
#     form = JobtypeForm(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             jobtype = form.save(commit=False)
#             jobtype.shiftplan = shiftplan
#             jobtype.save()
#             return redirect("defs:detail-jobtype", pk=jobtype.id)
#         else:
#             return render(request, "defs/jobtype_form.html", context={
#                 "form": form
#             })

#     context = {
#         "form": form,
#         "sp": shiftplan,
#         "jobtypes": jobtypes
#     }

#     return render(request, "defs/create_jobtype.html", context)

# @login_required
# def create_jobtype_form(request):
#     form = JobtypeForm()
#     context = {
#         "form": form
#     }
#     return render(request, "defs/jobtype_form.html", context)