"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import os

from xml.dom.minidom import parseString

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from PloneBackupRecoverManagement.configuration.models import Configuration
from PloneBackupRecoverManagement.recover.RecoverController import RecoverController

class CommonTestCase(TestCase):

    def setUp(self):
        # Other properties use the default value.
        import tempfile

        repository = os.path.join(tempfile.gettempdir(), 'repository')
        self.config = Configuration.objects.create(repository=repository, recover_script='')

        # Create simulation backup files for testing
        self.temp_backup_files = [
            '2011-11-06-02-10-30.deltafsz',
            '2011-10-10-02-10-30.fsz',
            '2011-10-09-08-50-20.deltafsz',
            '2011-10-08-10-22-22.deltafsz',
            '2011-10-07-08-10-10.deltafsz',
            '2011-09-20-10-10-10.fsz',
            '2011-09-12-10-30-44.fsz',
            '2011-09-10-08-08-08.deltafsz',
            '2011-09-02-03-03-03.deltafsz',
            '2011-08-10-06-17-40.fsz',
        ]
        self.temp_backup_files.sort()

        os.mkdir(repository)
        for filename in self.temp_backup_files:
            open(os.path.join(repository, filename), 'w+').close()

    def tearDown(self):
        repository = self.config.repository
        path_join = os.path.join
        for filename in self.temp_backup_files:
            os.remove(path_join(repository, filename))
        os.rmdir(repository)

class RecoverControllerTest(CommonTestCase):

    def test_can_delete_deltafsz_without_warning(self):
        rc = RecoverController()
        result, warning = rc.can_delete_before('2011-10-09-08-50-20.deltafsz')
        self.assertEqual(result, True)
        self.assertEqual(warning, False)

    def test_can_delete_deltafsz_with_warning(self):
        rc = RecoverController()
        result, warning = rc.can_delete_before('2011-10-07-08-10-10.deltafsz')
        self.assertEqual(result, True)
        self.assertEqual(warning, True)

    def test_can_not_delete_deltafsz(self):
        rc = RecoverController()
        result, warning = rc.can_delete_before('2011-11-06-02-30-30.deltafsz')
        self.assertEqual(result, False)
        self.assertEqual(warning, False)

    def test_can_delete_fsz(self):
        rc = RecoverController()
        result, warning = rc.can_delete_before('2011-09-12-10-30-44.fsz')
        self.assertEqual(result, True)
        self.assertEqual(warning, False)

    def test_can_not_delete_fsz(self):
        rc = RecoverController()
        result, warning = rc.can_delete_before('2011-09-20-10-10-10.fsz')
        self.assertEqual(result, False)
        self.assertEqual(warning, False)


class ViewTest(CommonTestCase):

    def setUp(self):
        super(ViewTest, self).setUp()

        User.objects.create_user('test', 'qcx@bjstats.gov.cn', 'test')
        self.client = Client()
        self.client.login(username='test', password='test')

    def test_ajax_api_can_delete_cannot_delete_fsz(self):
        resp = self.client.get('/recover/can_delete/2011-09-20-10-10-10.fsz/')
        self.assertEqual(resp.status_code, 200)

        xmldoc = parseString(resp.content)

        nodes = xmldoc.getElementsByTagName('can_delete')
        self.assertNotEqual(len(nodes), 0)
        self.assertEqual(nodes[0].firstChild.nodeValue, '0')

        nodes = xmldoc.getElementsByTagName('warning')
        self.assertNotEqual(len(nodes), 0)
        self.assertEqual(nodes[0].firstChild, None)

    def test_ajax_api_can_delete_can_delete_with_warning(self):
        resp = self.client.get('/recover/can_delete/2011-10-07-08-10-10.deltafsz/')
        self.assertEqual(resp.status_code, 200)

        xmldoc = parseString(resp.content)

        nodes = xmldoc.getElementsByTagName('can_delete')
        self.assertNotEqual(len(nodes), 0)
        self.assertEqual(nodes[0].firstChild.nodeValue, '1')

        nodes = xmldoc.getElementsByTagName('warning')
        self.assertNotEqual(len(nodes), 0)
        self.assertGreater(len(nodes[0].firstChild.nodeValue), 0)

    def test_ajax_api_can_delete_can_delete_without_warning(self):
        resp = self.client.get('/recover/can_delete/2011-10-09-08-50-20.deltafsz/')
        self.assertEqual(resp.status_code, 200)

        xmldoc = parseString(resp.content)

        nodes = xmldoc.getElementsByTagName('can_delete')
        self.assertNotEqual(len(nodes), 0)
        self.assertEqual(nodes[0].firstChild.nodeValue, '1')

        nodes = xmldoc.getElementsByTagName('warning')
        self.assertNotEqual(len(nodes), 0)
        self.assertIsNone(nodes[0].firstChild)

