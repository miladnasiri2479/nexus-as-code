#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Nexus lookup plugin - query existing Nexus resources.
"""

from ansible.plugins.lookup import LookupBase
import json

try:
    import urllib.request
    import urllib.error
    import base64
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        if not HAS_URLLIB:
            raise AnsibleError("urllib is required for nexus lookup")

        base_url = kwargs.get('base_url', 'http://localhost:8081')
        username = kwargs.get('username', 'admin')
        password = kwargs.get('password', '')
        resource_type = kwargs.get('resource_type', 'repository')

        api_url = f"{base_url.rstrip('/')}/service/rest/v1"

        resource_map = {
            'repository': '/repositories',
            'blobstore': '/blobstores',
            'user': '/security/users',
            'role': '/security/roles',
            'cleanup-policy': '/cleanup-policies',
        }

        endpoint = resource_map.get(resource_type, f'/{resource_type}')
        url = f"{api_url}{endpoint}"

        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        headers = {
            'Authorization': f'Basic {credentials}',
            'Accept': 'application/json',
        }

        req = urllib.request.Request(url, headers=headers)
        try:
            response = urllib.request.urlopen(req)
            data = json.loads(response.read().decode('utf-8'))
            if isinstance(data, list):
                return data
            return [data]
        except Exception as e:
            raise AnsibleError(f"Failed to query Nexus: {str(e)}")
