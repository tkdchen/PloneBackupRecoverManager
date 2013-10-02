import os
import sys

path = r'D:\mycode\websites'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'PloneBackupRecoverManagement.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
