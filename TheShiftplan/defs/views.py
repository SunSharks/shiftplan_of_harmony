from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import Jobtype, Job, SubCrew

from .forms import JobtypeForm, JobForm
# from .forms import TimeFormSet, JobtypeFormSet
from django.views import generic
from django.views.generic.edit import CreateView, FormView


# class IndexView(generic.ListView):
#     template_name = 'defs/index.html'
#     context_object_name = 'shiftplan_list'

#     def get_queryset(self):
#         """Return all available shiftplan instances."""
#         return Shiftplan.objects.all()

# # class ShiftplanCreateView(CreateView):
# #     model = Shiftplan
# #     # template_name = 'defs/time_interval_form.html'
# #     fields = ['name']


# class ShiftplanDefView(FormView):
#     model = Shiftplan
#     template_name = 'defs/shiftplan_def.html'
#     fields = ['name']


# class TimeIntervalCreateView(CreateView):
#     model = TimeInterval
#     # template_name = 'defs/time_interval_form.html'
#     fields = ['start_date', 'end_date']

# @login_required
# def create_shiftplan(request):
#     context = {}
#     return render(request, "defs/create_shiftplan.html", context)

# @login_required
# def shiftplan_def(request, pk):
#     links = ["time_def", "jobtype_def"]
#     shiftplan = get_object_or_404(Shiftplan, pk=pk)
#     if request.method == "POST":
#         try:
#             sp_name = request.POST['shiftplan_name']
#         except (KeyError, Shiftplan.DoesNotExist):
#             # Redisplay the question voting form.
#             return render(request, 'defs/shiftplan_def.html', {
#                 'sp': shiftplan,
#                 'error_message': "You didn't select a choice.",
#             })
#         else:
#             shiftplan.name = sp_name
#             shiftplan.save()
#             # Always return an HttpResponseRedirect after successfully dealing
#             # with POST data. This prevents data from being posted twice if a
#             # user hits the Back button.
#             return HttpResponseRedirect(reverse('defs:shiftplan_def', args=(shiftplan.id,)))

#     return render(request, 'defs/shiftplan_def.html', {'sp': shiftplan})

# # === TIME INTERVALS ===

# def time_interval_def(request, pk):
#     shiftplan = get_object_or_404(Shiftplan, pk=pk)
#     time_intervals = TimeInterval.objects.filter(shiftplan=shiftplan)
#     context = {
#         'sp': shiftplan,
#         'ti_list': time_intervals
#     }
#     return render(request, "defs/timeinterval_def.html", context)


# def create_time_interval(request, pk):
#     shiftplan = get_object_or_404(Shiftplan, pk=pk)
#     time_intervals = TimeInterval.objects.filter(shiftplan=shiftplan)
#     form = TimeIntervalForm(request.POST or None)

#     if request.method == "POST":
#         if form.is_valid():
#             ti = form.save(commit=False)
#             ti.shiftplan = shiftplan
#             ti.save()
#             return redirect("defs:ti_def", pk=shiftplan.id)

#     context = {
#         "form": form,
#         "sp": shiftplan,
#         "time_intervals": time_intervals
#     }

#     return render(request, "defs/create_time_interval.html", context)

# @login_required
# def create_time_interval_form(request):
#     form = TimeIntervalForm()
#     context = {
#         "form": form
#     }
#     return render(request, "defs/timeinterval_form.html", context)


# @login_required
# def update_time_interval(request, pk):
#     ti = TimeInterval.objects.get(id=pk)
#     form = TimeIntervalForm(request.POST or None, instance=ti)
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect("defs:ti_def", pk=ti.shiftplan.id)
#     context = {
#         "form": form,
#         "ti": ti
#     }

#     return render(request, "defs/timeinterval_form.html", context)


# # @login_required
# # def detail_time_interval(request, pk):
# #     jobtype = get_object_or_404(Jobtype, id=pk)
# #     context = {
# #         "jobtype": jobtype
# #     }
# #     return render(request, "defs/jobtype_detail.html", context)


# @login_required
# def delete_time_interval(request, pk):
#     ti = get_object_or_404(TimeInterval, id=pk)
#     if request.method == "POST":
#         ti.delete()
#         return HttpResponse("Time Interval deleted.")
#         # return redirect("defs:ti_def", pk=ti.shiftplan.id)

#     return HttpResponseNotAllowed(
#         [
#             "POST",
#         ]
#     )


# def time_def(request, pk):
#     shiftplan = get_object_or_404(Shiftplan, pk=pk)
#     tf_text = {"hourly": None, "block": None, "individual": None}
#     tf_text[shiftplan.time_format] = True
#     context = {'sp': shiftplan}
#     context.update(tf_text)
#     if request.method == "POST":
#         try:
#             tf = request.POST['time_def']
#         except (KeyError, Shiftplan.DoesNotExist):
#             # Redisplay the question voting form.
#             context.update({'error_message': "You didn't select a choice."})
#             return render(request, 'defs/time_def.html', context)
#         else:
#             shiftplan.time_format = tf
#             shiftplan.save()
#             return HttpResponseRedirect(reverse('defs:time-def', args=(shiftplan.id,)))
#     return render(request, 'defs/time_def.html', context)


# @login_required
# def jobtype_def(request, pk):
#     shiftplan = get_object_or_404(Shiftplan, pk=pk)
#     return render(request, 'defs/jobtype_def.html', {'sp': shiftplan})


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


# @login_required
# def update_jobtype(request, pk):
#     jobtype = Jobtype.objects.get(id=pk)
#     form = JobtypeForm(request.POST or None, instance=jobtype)
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect("defs:detail-jobtype", pk=jobtype.id)
#     context = {
#         "form": form,
#         "jobtype": jobtype
#     }

#     return render(request, "defs/jobtype_form.html", context)


# @login_required
# def detail_jobtype(request, pk):
#     jobtype = get_object_or_404(Jobtype, id=pk)
#     context = {
#         "jobtype": jobtype
#     }
#     return render(request, "defs/jobtype_detail.html", context)


# @login_required
# def delete_jobtype(request, pk):
#     jobtype = get_object_or_404(Jobtype, id=pk)
#     if request.method == "POST":
#         jobtype.delete()
#         return HttpResponse("")

#     return HttpResponseNotAllowed(
#         [
#             "POST",
#         ]
#     )


# @login_required
# def job_def(request, pk):
#     jobtype = get_object_or_404(Jobtype, pk=pk)
#     return render(request, 'defs/job_def.html', {'jobtype': jobtype})


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


# @login_required
# def create_job_form(request):
#     form = JobForm()
#     context = {
#         "form": form
#     }
#     return render(request, "defs/job_form.html", context)


# @login_required
# def update_job(request, pk):
#     job = Job.objects.get(id=pk)
#     form = JobForm(request.POST or None, instance=job)
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect("defs:detail-job", pk=job.id)
#     context = {
#         "form": form,
#         "job": job
#     }

#     return render(request, "defs/job_form.html", context)


# @login_required
# def detail_job(request, pk):
#     job = get_object_or_404(Job, id=pk)
#     context = {
#         "job": job
#     }
#     return render(request, "defs/job_detail.html", context)


# @login_required
# def delete_job(request, pk):
#     job = get_object_or_404(Job, id=pk)
#     if request.method == "POST":
#         job.delete()
#         return HttpResponse("")

#     return HttpResponseNotAllowed(
#         [
#             "POST",
#         ]
#     )

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
