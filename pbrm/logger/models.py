# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Log(models.Model):
    username = models.CharField(max_length=100, help_text=_('Who did the behavior that is associated with this log.'))
    when = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=8, db_index=True)
    succeeded = models.BooleanField(help_text=_('Whether the behavior with which this log is associated succeeded.'))
    detail = models.TextField(help_text=_('Holds the every thing that is printed into the stdout during the backup or recover process.'))

    def __unicode__(self):
        return u'%s at %s by %s' % (self.category, self.when, self.username)

# Helper functions
def log_log(user, category, succeeded, detail):
    log = Log()
    log.username = user.username
    log.category = category
    log.succeeded = succeeded
    log.detail = detail
    log.save()
    return log

def log_backup_log(user, succeeded, detail):
    return log_log(user, 'backup', succeeded, detail)

def log_recover_log(user, succeeded, detail):
    return log_log(user, 'recover', succeeded, detail)

def log_delete_log(user, succeeded, detail):
    return log_log(user, 'delete', succeeded, detail)
