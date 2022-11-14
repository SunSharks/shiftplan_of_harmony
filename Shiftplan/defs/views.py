from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader
from django.http import Http404

from .models import Shiftplan, TimeInterval, Jobtype, Job

from .forms import JobtypeForm
from .forms import TimeFormSet, JobtypeFormSet
from django.views import generic
from django.views.generic.edit import CreateView, FormView


class IndexView(generic.ListView):
    template_name = 'defs/index.html'
    context_object_name = 'shiftplan_list'

    def get_queryset(self):
        """Return all available shiftplan instances."""
        return Shiftplan.objects.all()


# def index(request):
#     shiftplan_list = Shiftplan.objects.all()
#     context = {
#         'shiftplan_list': shiftplan_list,
#     }
#     return render(request, 'defs/index.html', context)

#
class ShiftplanDefView(FormView):
    model = Shiftplan
    template_name = 'defs/shiftplan_def.html'
    fields = ['name']


class TimeIntervalCreateView(CreateView):
    model = TimeInterval
    # template_name = 'defs/time_interval_form.html'
    fields = ['start_date', 'end_date']


def shiftplan_def(request, shiftplan_id):
    links = ["time_def", "jobtype_def"]
    shiftplan = get_object_or_404(Shiftplan, pk=shiftplan_id)
    if request.method == "POST":
        try:
            sp_name = request.POST['shiftplan_name']
        except (KeyError, Shiftplan.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'defs/shiftplan_def.html', {
                'sp': shiftplan,
                'error_message': "You didn't select a choice.",
            })
        else:
            shiftplan.name = sp_name
            shiftplan.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('defs:shiftplan_def', args=(shiftplan.id,)))

    return render(request, 'defs/shiftplan_def.html', {'sp': shiftplan})


def add_time_interval(request, shiftplan_id):
    shiftplan = get_object_or_404(Shiftplan, pk=shiftplan_id)
    time_intervals = TimeInterval.objects.filter(shiftplan=shiftplan)
    formset = TimeFormSet(request.POST or None)

    if request.method == "POST":
        if formset.is_valid():
            formset.instance = shiftplan
            formset.save()
            return redirect("defs:ti_def", shiftplan_id=shiftplan.id)

    context = {
        "formset": formset,
        "sp": shiftplan,
        "time_intervals": time_intervals
    }

    return render(request, "defs/add_time_interval.html", context)


def time_def(request, shiftplan_id):
    shiftplan = get_object_or_404(Shiftplan, pk=shiftplan_id)
    tf_text = {"hourly": None, "block": None, "individual": None}
    tf_text[shiftplan.time_format] = True
    context = {'sp': shiftplan}
    context.update(tf_text)
    if request.method == "POST":
        try:
            tf = request.POST['time_def']
        except (KeyError, Shiftplan.DoesNotExist):
            # Redisplay the question voting form.
            context.update({'error_message': "You didn't select a choice."})
            return render(request, 'defs/time_def.html', context)
        else:
            shiftplan.time_format = tf
            shiftplan.save()
            return HttpResponseRedirect(reverse('defs:time-def', args=(shiftplan.id,)))
    return render(request, 'defs/time_def.html', context)


def jobtype_def(request, pk):
    shiftplan = get_object_or_404(Shiftplan, pk=pk)
    return render(request, 'defs/jobtype_def.html', {'sp': shiftplan})


def create_jobtype(request, pk):
    shiftplan = get_object_or_404(Shiftplan, pk=pk)
    jobtypes = Jobtype.objects.filter(shiftplan=shiftplan)
    form = JobtypeForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            jobtype = form.save(commit=False)
            jobtype.shiftplan = shiftplan
            jobtype.save()
            return redirect("defs:detail-jobtype", pk=jobtype.id)
        else:
            return render(request, "defs/jobtype_form.html", context={
                "form": form
            })

    context = {
        "form": form,
        "sp": shiftplan,
        "jobtypes": jobtypes
    }

    return render(request, "defs/create_jobtype.html", context)


def create_jobtype_form(request):
    form = JobtypeForm()
    context = {
        "form": form
    }
    return render(request, "defs/jobtype_form.html", context)


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


def detail_jobtype(request, pk):
    jobtype = get_object_or_404(Jobtype, id=pk)
    context = {
        "jobtype": jobtype
    }
    return render(request, "defs/jobtype_detail.html", context)


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


def job_def(request, shiftplan_id):
    return HttpResponse("Job Definition")
