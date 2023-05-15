from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import Jobtype, Job, SubCrew, UserProfile

from .forms import JobtypeForm, JobForm
from django.views import generic
from django.views.generic.edit import CreateView, FormView


@login_required
def index_view(request):
    context = {}
    return render(request, 'defs/index.html', context)


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

# @login_required
# def bulk_create_jobs(request, pk):
#     jobtype = get_object_or_404(Jobtype, id=pk)
#     time_intervals = TimeInterval.objects.filter(shiftplan=jobtype.shiftplan)
#     print("time_intervals: ", time_intervals)
#     context = {
#         "time_intervals_exist": not not time_intervals,
#         "ti_list": time_intervals,
#         "jobtype": jobtype,
#         "days": []
#     }
#     return render(request, "defs/bulk_create_jobs.html", context)
