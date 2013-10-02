"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from datetime import datetime

from logger.models import Log

class LoggerTest(TestCase):

    def testInsertExpectedBackupLog(self):
        log = Log()
        log.category = 'backup'
        log.detail = 'Backup successful'
        log.succeeded = True
        log.save()
        
        self.assertNotEqual(log.id, 0)

    def testInsertExpectedRecoverLog(self):
        log = Log()
        log.category = 'recover'
        log.detail = 'Recover successful'
        log.succeeded = True
        log.save()
        
        self.assertNotEqual(log.id, 0)
