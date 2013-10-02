# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _

import os

from PloneBackupRecoverManagement.configuration.models import Configuration
from PloneBackupRecoverManagement.logger.models import Log
from PloneBackupRecoverManagement.logger.models import log_recover_log, log_delete_log

class RecoverController(object):

    def __init__(self):
        self.config = Configuration.getConfiguration()

    def getBackupFiles(self):
        '''Retrieve all avialable backup files'''

        import glob

        basename = os.path.basename
        glob_ = glob.glob
        pattern = os.path.join(self.config.repository, '*fsz')
        filenames = [basename(filename)
                     for filename in glob_(pattern)]
        filenames.sort(reverse=True)
        return filenames

    # TODO: Need to refact this and next method. Merge them into one method.
    def _has_fsz_after(self, filename):
        filenames = os.listdir(self.config.repository)
        filenames.sort()

        k = None
        for i in range(len(filenames)):
            if filenames[i] == filename:
                k = i
                break

        # The filename does not exist in the backup directory.
        # This case should not occur under any circumstance.
        if not k:
            return False

        for i in range(k + 1, len(filenames)):
            if filenames[i].endswith('.fsz'):
                return True
        return False

    def _has_deltafsz_after(self, filename):
        filenames = os.listdir(self.config.repository)
        filenames.sort()

        k = None
        for i in range(len(filenames)):
            if filenames[i] == filename:
                k = i
                break

        # The filename does not exist in the backup directory.
        # This case should not occur under any circumstance.
        if not k: return False

        k += 1
        # If the filename is the last one, there is no deltafsz certainly.
        if k >= len(filenames): return False

        return filenames[k].endswith('.deltafsz')

    def _can_delete_fsz(self, filename):
        # 完整备份之后没有差异备份，并且有完整备份
        can_delete = not self._has_deltafsz_after(filename) and \
                self._has_fsz_after(filename)
        warning = False # No warning for this case.
        return (can_delete, warning)

    def _can_delete_deltafsz(self, filename):
        # 差异备份之后有完整备份
        # Warning：如果删除差异备份之前的所有备份文件，
        # 将导致该差异备份与其后的完整备份之间的任何差
        # 异备份无法恢复，即这部分数据将丢失
        can_delete = self._has_fsz_after(filename)
        warning = self._has_deltafsz_after(filename)
        return (can_delete, warning)

    def can_delete_before(self, filename):
        if filename.endswith('.fsz'):
            return self._can_delete_fsz(filename)
        else:
            return self._can_delete_deltafsz(filename)

    def do_delete_before(self, by_who, filename):
        can_delete, warning = self.can_delete_before(filename)

        if can_delete:
            repository = self.config.repository

            # Collect file names to delete
            filenames = os.listdir(repository)
            filenames.sort()
            del_candidates = []
            for item in filenames:
                del_candidates.append(item)
                if item == filename:
                    break

            # Delete them
            path_join = os.path.join
            for item in del_candidates:
                os.remove(path_join(repository, item))

            log = log_delete_log(user = by_who,
                                 succeeded = True,
                                 detail = _('The following backup files was deleted.%s') % \
                                            '\n'.join([''] + del_candidates))

        else:
            log = log_delete_log(user = by_who,
                                 succeeded = False,
                                 detail = _('The backup file and the older ones cannot be deleted.'))

        return log

    def do_recover(self, by_who, to_date):
        '''Recover Plone site to the state of date.

           This action will not unlock system from
           doing backup and recover until the process ends.
        '''

        import tempfile
        import subprocess

        # Creating the recover script and then run it in a subprocess.
        # TODO: This is not cross-platform.
        fd, filename = tempfile.mkstemp('_plone_recover.bat')
        os.write(fd, self.config.recover_script)
        os.close(fd)

        configuration = Configuration.getConfiguration()
        po = subprocess.Popen([filename,
                               configuration.plone_install_path,
                               configuration.repository,
                               to_date],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        stdout_data, stderr_data = po.communicate()

        log = log_recover_log(
            user = by_who,
            succeeded = po.returncode == 0,
            detail = '\n'.join(
                (stdout_data, stderr_data,
                _('Plone site has been recovered to %s') % to_date)))

        os.remove(filename)

        return log

