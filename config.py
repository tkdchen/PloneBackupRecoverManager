# -*- coding: utf-8 -*-

project_context = {
    'win32': {
        'datafile': r'D:\mycode\websites\PloneBackupRecoverManagement\data\management.db',
        'templates': r'D:\mycode\websites\PloneBackupRecoverManagement\templates',
        'resources': r'D:\mycode\websites\PloneBackupRecoverManagement\statics',
    },

    'unix': {
        'datafile': '/home/chenxiong/mycode/websites/PloneBackupRecoverManagement/data/management.db',
        'templates': '/home/chenxiong/mycode/websites/PloneBackupRecoverManagement/templates',
        'resources': '/home/chenxiong/mycode/websites/PloneBackupRecoverManagement/statics',
    },
}

class _project_context(object):
    def __init__(self, context):
        self._context = context

    def __getattr__(self, name):
        return self._context[name]

def get_project_context():
    import sys

    return _project_context(
        project_context['win32' if sys.platform == 'win32' else 'unix'])
