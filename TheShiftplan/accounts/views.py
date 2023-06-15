import logging

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .models import UserCandidate
from .forms import RegisterForm
from .users_tableplot import *

def registration_view(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'accounts/register.html', { 'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/register.html', {'form': form})

@login_required
def users_table_view(request):
    context = {}
    user_candidates = [uc.as_dict() for uc in UserCandidate.objects.all()]
    session = request.session
    djaploda = session.get('django_dash', {})
    # new_user_cands = djaploda.get('user_candidates', user_candidates)
    # new_user_cands = user_candidates
    djaploda['user_candidates'] = user_candidates
    session['django_dash'] = djaploda
    # logging.debug(session["django_dash"])
    return render(request, 'accounts/users_table.html', context)