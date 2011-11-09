# -*- coding: utf-8 -*-

from django import forms
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

from django.utils.translation import ugettext_lazy as _

from PloneBackupRecoverManagement.logger.models import Log

class LogFilterForm(forms.Form):
    when = forms.DateField(label=_('Logged when'),
                           required=False,
                           input_formats='%Y-%m-%d')
    category = forms.ChoiceField(label=_('Log category'),
                                 choices=(
                                     ('-', _('Not select')),
                                     ('backup', _('Backup')),
                                     ('recover', _('Recover')),
                                 ))
    succeeded = forms.ChoiceField(label=_('Succeeded'),
        choices=(
            ('-', _('Not select')),
            ('yes', _('Yes')),
            ('no', _('No'))
        ))

@login_required
def index(request):
    c = {}
    c.update(csrf(request))

    logs = []

    if request.method == 'POST':
        form = LogFilterForm(request.POST)

        if form.is_valid():
            conditions = []

            when = form.cleaned_data['when']
            if when:
                conditions.append(Q(when=when))

            category = form.cleaned_data['category']
            if category != '-':
                conditions.append(Q(category=category))

            succeeded = form.cleaned_data['succeeded']
            if succeeded != '-':
                conditions.append(Q(succeeded=True if succeeded == 'yes' else False))

            if conditions:
                logs = Log.objects.filter(
                    reduce(lambda x, y: x & y, conditions)).order_by('-when')
            else:
                logs = Log.objects.all().order_by('-when')

    else:
        form = LogFilterForm()
        logs = Log.objects.all().order_by('-when')

    c['form'] = form
    c['logs'] = logs
    c['user'] = request.user
    return render_to_response('logger/index.html', c)
