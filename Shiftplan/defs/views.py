from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404

from .models import Shiftplan, Jobtype, Job


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)


def index(request):
    shiftplan_list = Shiftplan.objects.all()
    context = {
        'shiftplan_list': shiftplan_list,
    }
    return render(request, 'defs/index.html', context)


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


def jobtype_def(request, shiftplan_id):
    shiftplan = get_object_or_404(Shiftplan, pk=shiftplan_id)
    return render(request, 'defs/jobtype_def.html', {'sp': shiftplan})


def job_def(request, shiftplan_id):
    return HttpResponse("Job Definition")


# ...
