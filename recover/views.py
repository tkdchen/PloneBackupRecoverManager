# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _

from PloneBackupRecoverManagement.configuration.models import Configuration
from PloneBackupRecoverManagement.recover.RecoverController import RecoverController
from PloneBackupRecoverManagement.logger.models import Log, log_delete_log

@login_required
def index(request):
    c = {}
    c.update(csrf(request))

    rc = RecoverController()
    c['backup_files'] = rc.getBackupFiles()

    logs = Log.objects.filter(category='recover').order_by('-when')[0:1]

    c['user'] = request.user
    return render_to_response('recover/index.html', c)

def do_recover(request):
    # TODO: check it
    recover_to = request.POST['recover_to']
    recover_to_date = recover_to.split('.')[0]
    rc = RecoverController()
    return rc.do_recover(request.user, recover_to_date)

def do_delete(request):
    backup_file = request.POST['recover_to']
    rc = RecoverController()
    return rc.do_delete_before(request.user, backup_file)

@login_required
def do_command(request):
    if request.method == 'POST':
        commands = { 'recover': do_recover, 'delete': do_delete }
        # TODO: Check whether the system is locked first. Not implemented.
        log = commands[request.POST['do_command']](request)

        c = {}
        c.update(csrf(request))

        rc = RecoverController()
        c['backup_files'] = rc.getBackupFiles()
        c['log'] = log
        c['user'] = request.user
        return render_to_response('recover/index.html', c)

    return index(request)

@login_required
def can_delete(request, filename):
    rc = RecoverController()
    can_delete, warning = rc.can_delete_before(filename)

    buf = '''<resp for="can_delete">
        <can_delete>%s</can_delete>
        <warning>%s</warning>
    </resp>''' % ('1' if can_delete else '0', _('Warning: After deleting files, the data contained in the file between the deleted file and the most close full backup file will be lost.') if warning else '')

    return HttpResponse(buf, content_type='text/xml; charset=utf-8')
