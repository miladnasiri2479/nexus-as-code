#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Nexus Repository Manager filters for Ansible.

Provides utility filters for Nexus configuration processing.
"""

from ansible.errors import AnsibleError
import json


def nexus_merge_defaults(config, *defaults_list):
    """Deep merge configuration with defaults. Config overrides defaults."""
    result = {}
    for defaults in defaults_list:
        if isinstance(defaults, dict):
            result.update(defaults)
    if isinstance(config, dict):
        result.update(config)
    return result


def nexus_to_json(data, indent=2):
    """Convert dict to formatted JSON string."""
    return json.dumps(data, indent=indent, default=str)


def nexus_from_json(data):
    """Parse JSON string to dict."""
    if isinstance(data, str):
        return json.loads(data)
    return data


class FilterModule(object):
    def filters(self):
        return {
            'nexus_merge_defaults': nexus_merge_defaults,
            'nexus_to_json': nexus_to_json,
            'nexus_from_json': nexus_from_json,
        }
