import pandas as pd

from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader
from django.http import Http404
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Jobtype, Job, SubCrew, UserProfile

from .forms import JobtypeForm, JobForm
from django.views import generic
from django.views.generic.edit import CreateView, FormView

from .defplot import *
# @login_required
# def index_view(request):
#     context = {}
#     return render(request, 'defs/index.html', context)


@login_required
def jobtype_def(request):
    jobtypes = Jobtype.objects.all()
    form = JobtypeForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            jobtype = form.save(commit=False)
            jobtype.save()
            jobtypes = Jobtype.objects.all()
            context = {
                "form": form,
                "jobtypes": jobtypes
            }

            return render(request, "defs/single_jobtype.html", {"jt": jobtype})
        else:
            return render(request, "defs/jobtype_def.html", context={
                "form": form,
                "jobtypes": jobtypes
            })

    context = {
        "form": form,
        "jobtypes": jobtypes
    }

    return render(request, "defs/jobtype_def.html", context)


@login_required
def create_jobtype_form(request):
    form = JobtypeForm()
    context = {
        "form": form
    }
    return render(request, "defs/jobtype_form.html", context)


@login_required
def update_jobtype(request, pk):
    jobtype = Jobtype.objects.get(id=pk)
    form = JobtypeForm(request.POST or None, instance=jobtype)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("defs:detail-jobtype", pk=jobtype.id)
    context = {
        "form": form,
        "jobtype": jobtype
    }

    return render(request, "defs/jobtype_form.html", context)


@login_required
def detail_jobtype(request, pk):
    jobtype = get_object_or_404(Jobtype, id=pk)
    context = {
        "jobtype": jobtype
    }
    return render(request, "defs/jobtype_detail.html", context)


@login_required
def delete_jobtype(request, pk):
    jobtype = get_object_or_404(Jobtype, id=pk)
    if request.method == "POST":
        jobtype.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )


@login_required
def job_def(request, pk):
    jobtype = get_object_or_404(Jobtype, pk=pk)
    jobs = Job.objects.filter(jobtype=jobtype)
    form = JobForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            job = form.save(commit=False)
            job.jobtype = jobtype
            job.save()
            return render(request, "defs/single_job.html", {"j": job})
            # return redirect("defs:detail-job", pk=jobtype.id)
        else:
            return render(request, "defs/job_def.html", context={
                "form": form,
                "jobtype": jobtype
            })
    return render(request, 'defs/job_def.html', {"form": form,'jobtype': jobtype})


# @login_required
# def create_job(request, pk):
#     jobtype = get_object_or_404(Jobtype, pk=pk)
#     jobs = Job.objects.filter(jobtype=jobtype)
#     form = JobForm(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             job = form.save(commit=False)
#             job.jobtype = jobtype
#             job.save()
#             return HttpResponse("success")
#             # return redirect("defs:detail-job", pk=jobtype.id)
#         else:
#             # return render(request, "defs/jobtype_form.html", context={
#             #     "form": form
#             # })
#             return HttpResponse("fail")

#     context = {
#         "form": form,
#         "jobtype": jobtype
#     }

#     return render(request, "defs/create_job.html", context)


@login_required
def create_job_form(request):
    form = JobForm()
    context = {
        "form": form
    }
    return render(request, "defs/job_form.html", context)


@login_required
def update_job(request, pk):
    job = Job.objects.get(id=pk)
    form = JobForm(request.POST or None, instance=job)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("defs:detail-job", pk=job.id)
    context = {
        "form": form,
        "job": job
    }

    return render(request, "defs/job_form.html", context)


@login_required
def detail_job(request, pk):
    job = get_object_or_404(Job, id=pk)
    context = {
        "job": job
    }
    return render(request, "defs/job_detail.html", context)


@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, id=pk)
    if request.method == "POST":
        job.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )

@login_required
def index_view(request, **kwargs):
    # request.session.flush()
    current_user = request.user if type(request.user) is not AnonymousUser else None
    jobtypes = Jobtype.objects.all()
    if len(jobtypes) == 0:
        return HttpResponse('<h1>No Jobtypes defined.</h1>') 
    jobs_allowed = []
    for jt in jobtypes:
        if jt.subcrew:
            # print(current_user in jt.subcrew.members.all())
            if not current_user in jt.subcrew.members.all():
                continue
        # print(jt.job_set.all().values_list("pk", flat=True))
        jobs_allowed.extend(jt.job_set.all())
    if len(jobs_allowed) == 0:
        return HttpResponse('<h1>No Jobs defined.</h1>') 
    ok_job_qs = Q()
    for job_pk in jobs_allowed:
        ok_job_qs = ok_job_qs | Q(pk=job_pk.pk)
    # user_ratings = UserJobRating.objects.filter(ok_job_qs)
    # print(50*'+')
    allowed_jobs = Job.objects.filter(ok_job_qs)
    print(allowed_jobs)
    l = []
    for j in allowed_jobs:
        d = j.as_dict()
        jobtype = j.jobtype.as_dict()
        d.update(jobtype)
        l.append(d)

    df = pd.DataFrame(l)
    df['begin'] = pd.to_datetime(df['begin_date'].astype(str) + ' ' + df['begin_time'].astype(str))
    df['end'] = pd.to_datetime(df['end_date'].astype(str) + ' ' + df['end_time'].astype(str))
    # df['during'] = df.end - df.begin
    
    # print("CONVERT TO JSON")
    df['begin'] = df['begin'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['end'] = df['end'].dt.strftime('%Y-%m-%d %H:%M:%S')
    context = {"jt_descriptions": [{"name": n, "description": d} for n, d in zip(df['name'], df['description'])]
        # df.loc[df.index==i]["name"]: df.loc[df.index==i]["description"] for i in df.index
    }
    # print(type(df["user"][0]))
    df = df.to_json()
    # print(context)
    session = request.session
    djaploda = session.get('django_dash', {})
    ndf = djaploda.get('df', df)
    ndf = df
    djaploda['df'] = ndf
    session['django_dash'] = djaploda  
    # print(5*'---\n')
    return render(request, 'defs/index.html', context)