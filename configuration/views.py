# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _

from PloneBackupRecoverManagement.configuration.models import Configuration
from PloneBackupRecoverManagement.logger.models import log_log

class ConfigurationForm(ModelForm):
    class Meta:
        model = Configuration

@login_required
def index(request):
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':
        form = ConfigurationForm(request.POST)
        if form.is_valid():
            try:
                configuration = Configuration.objects.get(pk=1)
            except Configuration.DoesNotExist:
                configuration = Configuration()

            configuration.repository = form.cleaned_data['repository']
            configuration.plone_install_path = form.cleaned_data['plone_install_path']
            configuration.backup_script = form.cleaned_data['backup_script']
            configuration.recover_script = form.cleaned_data['recover_script']

            try:
                configuration.save()
                log_log(request.user, 'configuration', True, _('Configuration has been saved.'))
            except Exception, err_msg:
                log_log(request.user,
                        'configuration',
                        False,
                        _('Saving configuration failed.\n'
                          'System error message is\n%(err_msg)s\n\n'
                          'You entered:\n'
                          'Plone installation path: %(plone_install_path)s\n'
                          'Backup file repository: %(repository)s') % {
                              'err_msg': err_msg,
                              'plone_install_path': configuration.plone_install_path,
                              'repository': configuration.repository})

    else:
        configuration = None
        try:
            configuration = Configuration.objects.get(pk=1)
        except Configuration.DoesNotExist:
            pass

        form = ConfigurationForm(instance=configuration)

    c['form'] = form
    c['user'] = request.user

    return render_to_response('configuration/index.html', c)
