# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Configuration(models.Model):
    plone_install_path = models.CharField(_('Plone installation Path'),
                                          max_length=50,
                                          default='D:\\Plone3',
                                          help_text=_('Where the Plone is installed. It should an absolute path. The path \'D:\\Plone3\' is recommended.'))

    repository = models.CharField(_('Repository'),
                                  max_length=50,
                                  default='D:\\Plone3_backup',
                                  help_text=_('The directory that holds backup files.'))

    backup_script = models.TextField(_('Backup script'), blank=True, null=True,
                                     help_text=_('The backup script is optional.'))

    recover_script = models.TextField(_('Recover script'),
        help_text=_('You must provide a recover script. You should ensure that the script has proper permission to finish the recover tasks.'))

    def __unicode__(self):
        return 'Configuration for backup and recover Plone site.'

    @staticmethod
    def getConfiguration():
        return Configuration.objects.get(pk=1)
