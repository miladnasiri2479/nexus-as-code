#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Nexus Audit Callback Plugin for Ansible.

Logs all API calls to Nexus for audit trail.
"""

from ansible.plugins.callback import CallbackBase
import json
import os
from datetime import datetime


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'nexus_audit'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.log_file = os.environ.get('NEXUS_AUDIT_LOG', '/var/log/nexus-ansible-audit.log')
        self._ensure_log_dir()

    def _ensure_log_dir(self):
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    def _write_log(self, entry):
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(entry, default=str) + '\n')
        except Exception:
            pass

    def v2_runner_on_ok(self, result):
        task_name = result._task.get_name() if result._task else 'unknown'
        if 'nexus' in task_name.lower():
            self._write_log({
                'timestamp': datetime.utcnow().isoformat(),
                'host': result._host.get_name(),
                'task': task_name,
                'status': 'ok',
                'changed': result._result.get('changed', False),
            })

    def v2_runner_on_failed(self, result, ignore_errors=False):
        task_name = result._task.get_name() if result._task else 'unknown'
        if 'nexus' in task_name.lower():
            self._write_log({
                'timestamp': datetime.utcnow().isoformat(),
                'host': result._host.get_name(),
                'task': task_name,
                'status': 'failed',
                'msg': result._result.get('msg', ''),
            })
