# -*- coding: utf-8 -*-

class Lock(object):

    def __init__(self, for_):
        self._pid_file = self._create_pid_file()
        self._lock_for = for_

    def _create_pid_file(self):
        pass

    def get_lock_file_name_for(behavior):
        pass

    def is_behavior_locked(behavior):
        pass

    def lock_system_for(behavior):
        pass

    def unlock_system_for(behavior):
        pass
