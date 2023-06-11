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

from .forms import UploadFileForm, JobtypeForm, JobForm, SubCrewForm
from django.views import generic
from django.views.generic.edit import CreateView, FormView

from .defplot import *

from accounts.models import UserCandidate, CandidatesList
from utils import upload_data
from utils import config

@login_required
def index_view(request, **kwargs):
    # request.session.flush()
    # print(request.FILES)
    context = {}
    current_user = request.user if type(request.user) is not AnonymousUser else None
    jobtypes = Jobtype.objects.all()
    if len(jobtypes) == 0:
        return HttpResponse('<h1>No Jobtypes defined.</h1>') 
    jobs_allowed = []
    jt_descriptions = []
    for jt in jobtypes:
        jt_descriptions.append({
            "description": jt.description,
            "name": jt.name
            })
        jobs_allowed.extend(jt.job_set.all())
    if len(jobs_allowed) == 0:
        return HttpResponse('<h1>No Jobs defined.</h1>') 
    prepare_djaploda_session_var(request, jobs_allowed, 'defs/index')
    # print(5*'---\n')
    
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            upload = upload_data.Upload(file)
            success, inst = upload.get_result_df_or_error()
            if success:
                create_candidate_instances(file, inst)
                context.update({
                    "upload_file": file.name
                })
            else:
                context.update({
                    "upload_error": inst
                })
    else:
        form = UploadFileForm()

    context.update({
        "jt_descriptions": jt_descriptions,
        "upload_file_form": form
    })
    return render(request, 'defs/index.html', context)

    
def create_candidate_instances(file, df):
    print(df)
    fname = file.name.split(".")[0]
    conflicting = CandidatesList.objects.filter(name=fname)
    conflicting.delete()
    cand_list = CandidatesList(name=fname, file=file)
    cand_list.save()
    renames = {}
    for c in df.columns:
        if c.lower() in config.file_to_code_dict:
            renames[c] = config.file_to_code_dict[c.lower()]
    # print(renames)
    df = df.rename(columns=renames)
    for i in df.index:
        user_cand = UserCandidate()
        for attr_name in renames.values():
            setattr(user_cand, attr_name, df.iloc[i][attr_name])
        setattr(user_cand, "candidates_list", cand_list)
        print(user_cand)
        user_cand.save()


@login_required
def upload_persons_view(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect("/success/url/")
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})
   

@login_required
def jobtype_def(request):
    jobtypes = Jobtype.objects.all()
    subcrews_context = {}
    for jt in jobtypes:
        subcrews_context.update(
            {
                jt.id: (jt.subcrew.id if jt.restricted_to_subcrew else  None)
            }
            )
    form = JobtypeForm(request.POST or None)
    print([jt.subcrew for jt in jobtypes])
    subcrews = [jt.subcrew for jt in jobtypes]
    if request.method == "POST":
        if form.is_valid():
            jobtype = form.save(commit=False)
            jobtype.save()
            jobtypes = Jobtype.objects.all()
            
            context = {
                "form": form,
                "jobtypes": jobtypes,
                "subcrews_context": subcrews_context
            }

            return render(request, "defs/single_jobtype.html", {"jt": jobtype})
        else:
            return render(request, "defs/jobtype_form.html", context={
                "form": form
            })

    context = {
        "form": form,
        "jobtypes": jobtypes,
        "subcrews_context": subcrews_context
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
    # for jt in jobtypes:
    #     subcrews_context.update(
    #         {
    #             jt.id: (jt.subcrew.id if jobtype.restricted_to_subcrew else  None)
    #         }
    #         )
    try:
        subcrew_id = jobtype.subcrew.id
    except:
        subcrew_id = None
    context = {
        "jobtype": jobtype,
        "subcrew_id": subcrew_id
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
            return render(request, "defs/job_form.html", context={
                "form": form,
            })
    return render(request, 'defs/job_def.html', {"form": form,'jobtype': jobtype})


@login_required
def visual_job_def(request, pk):
    jobtype = get_object_or_404(Jobtype, pk=pk)
    jobs = Job.objects.filter(jobtype=jobtype)
    prepare_djaploda_session_var(request, jobs, 'defs/job_def')
    session = request.session
    djaploda = session.get('django_dash', {})
    djaploda['jobtype'] = pk
    session['django_dash'] = djaploda
    return render(request, 'defs/visual_job_def.html', {'jobtype': jobtype})


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
def subcrew_def(request):
    subcrews = SubCrew.objects.all()
    form = SubCrewForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            subcrew = form.save()
            subcrews = SubCrew.objects.all()
            context = {
                "subcrew": subcrew
            }
            return render(request, "defs/single_subcrew.html", context)
        else:
            context = {
                "form": form
            }
            return render(request, "defs/subcrew_form.html", context)

    context = {
        "form": form,
        "subcrews": subcrews
    }

    return render(request, "defs/subcrew_def.html", context)


@login_required
def create_subcrew_form(request):
    form = SubCrewForm()
    context = {
        "form": form
    }
    return render(request, "defs/subcrew_form.html", context)


@login_required
def update_subcrew(request, pk):
    subcrew = get_object_or_404(SubCrew, id=pk)
    # print("members: ", subcrew.members.all())
    form = SubCrewForm(request.POST or None, instance=subcrew, initial={"members": [m.id for m in subcrew.members.all()]})
    if request.method == "POST":
        if form.is_valid():
            form.save()
            # subcrew = SubCrew.objects.get(id=pk)
            return redirect("defs:detail-subcrew", pk=subcrew.id)
    context = {
        "form": form,
        "subcrew": subcrew
    }

    return render(request, "defs/subcrew_form.html", context)


@login_required
def detail_subcrew(request, pk):
    subcrew = get_object_or_404(SubCrew, id=pk)
    print(subcrew.jobtype_set.all())
    context = {
        "subcrew": subcrew,
        "jobtypes": subcrew.jobtype_set.all()
    }
    return render(request, "defs/subcrew_detail.html", context)


@login_required
def inline_detail_subcrew(request, pk):
    subcrew = get_object_or_404(SubCrew, id=pk)
    print(subcrew.jobtype_set.all())
    context = {
        "subcrew": subcrew,
        "jobtypes": subcrew.jobtype_set.all(),
        "inline": True
    }
    return render(request, "defs/subcrew_detail.html", context)


@login_required
def toggle_inline_detail_subcrew(request, pk):
    return HttpResponse("")


@login_required
def delete_subcrew(request, pk):
    subcrew = get_object_or_404(SubCrew, id=pk)
    if request.method == "POST":
        subcrew.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )


@login_required
def prepare_djaploda_session_var(request, jobs_allowed, mode):
    ok_job_qs = Q()
    for job_pk in jobs_allowed:
        ok_job_qs = ok_job_qs | Q(pk=job_pk.pk)
    allowed_jobs = Job.objects.filter(ok_job_qs)
    # print(allowed_jobs)
    l = []
    for j in allowed_jobs:
        d = j.as_dict()
        d["job"] = j.pk
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

    df = df.to_json()
    # print(context)
    session = request.session
    djaploda = session.get('django_dash', {})
    ndf = djaploda.get('df', df)
    ndf = df
    djaploda['df'] = ndf
    djaploda['mode'] = mode
    session['django_dash'] = djaploda

