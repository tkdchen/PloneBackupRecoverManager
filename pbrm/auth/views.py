# -*- coding: utf-8 -*-

from django.core.context_processors import csrf
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_
from django.contrib.auth import logout as logout_
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


def login(request):
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login_(request, form.get_user())
            return HttpResponseRedirect(
                request.GET['next'] if 'next' in request.GET else '/recover/')

    else:
        form = AuthenticationForm()

    c['form'] = form
    return render_to_response('auth/login.html', c)

def logout(request):
    logout_(request)
    return HttpResponseRedirect('/login/')
