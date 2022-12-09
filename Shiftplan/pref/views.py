from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.db.models import Avg, Max, Min, Sum
from defs.models import Shiftplan, TimeInterval, Jobtype, Job
# Create your views here.


# class IndexView(generic.ListView):
#     template_name = 'pref/index.html'
#     # context_object_name = 'shiftplan_list'
#
#     # def get_queryset(self):
#     #     """Return all available shiftplan instances."""
#     #     return Shiftplan.objects.all()
# def index(request):
#     return render(request, 'pref/index.html')

class IndexView(generic.ListView):
    template_name = 'pref/index.html'
    context_object_name = 'shiftplan_list'

    def get_queryset(self):
        """Return all available shiftplan instances."""
        return Shiftplan.objects.all()

def tab_view(request, pk):
    shiftplan = get_object_or_404(Shiftplan, pk=pk)
    jts = shiftplan.jobtype_set.all()
    print(jts)
    jobs = Job.objects.filter(jobtype__shiftplan=shiftplan).distinct().all()
    print(list(jobs.aggregate(Max('begin')).values())[0].date())
    days = list(Job.objects.order_by('begin'))
    days = [d.begin.date for d in days if d.begin.date not in days]
    print(days)
    return render(request, 'pref/tab.html', {'sp': shiftplan, 'days': days})