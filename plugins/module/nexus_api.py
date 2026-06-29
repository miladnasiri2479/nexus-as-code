#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Nexus Repository Manager API Module for Ansible.

Provides idempotent management of Nexus resources via REST API.
Used internally by all nexus_* roles.
"""

from ansible.module_utils.basic import AnsibleModule
import json
import time
import base64

try:
    import urllib.request
    import urllib.error
    import urllib.parse
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False


def make_request(url, method='GET', data=None, headers=None, auth=None, validate_certs=True):
    """Make HTTP request to Nexus API."""
    if headers is None:
        headers = {}

    if auth:
        credentials = base64.b64encode(
            f"{auth[0]}:{auth[1]}".encode()
        ).decode()
        headers['Authorization'] = f'Basic {credentials}'

    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'

    if data is not None:
        data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        response = urllib.request.urlopen(req)
        response_data = response.read().decode('utf-8')
        return {
            'status': response.getcode(),
            'data': json.loads(response_data) if response_data else {},
            'changed': False
        }
    except urllib.error.HTTPError as e:
        response_data = e.read().decode('utf-8') if e.fp else ''
        return {
            'status': e.code,
            'data': json.loads(response_data) if response_data else {},
            'error': str(e),
            'changed': False
        }
    except urllib.error.URLError as e:
        return {
            'status': 0,
            'data': {},
            'error': str(e.reason),
            'changed': False
        }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            base_url=dict(type='str', default='http://localhost:8081'),
            username=dict(type='str', default='admin'),
            password=dict(type='str', required=True, no_log=True),
            operation=dict(type='str', required=True, choices=['create', 'update', 'delete', 'get', 'list']),
            resource_type=dict(type='str', required=True),
            name=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            body=dict(type='dict', default={}),
            validate_certs=dict(type='bool', default=True),
        ),
        required_if=[
            ('operation', ['create', 'update'], ['name', 'body']),
            ('operation', ['delete', 'get'], ['name']),
        ],
        supports_check_mode=True,
    )

    if not HAS_URLLIB:
        module.fail_json(msg="urllib is required for this module")

    base_url = module.params['base_url'].rstrip('/')
    username = module.params['username']
    password = module.params['password']
    operation = module.params['operation']
    resource_type = module.params['resource_type']
    name = module.params['name']
    state = module.params['state']
    body = module.params['body']

    api_base = f"{base_url}/service/rest/v1"

    # Map resource types to API endpoints
    resource_map = {
        'repository': '/repositories',
        'blobstore': '/blobstores',
        'user': '/security/users',
        'role': '/security/roles',
        'cleanup-policy': '/cleanup-policies',
        'realm': '/security/realms/active',
    }

    endpoint = resource_map.get(resource_type, f'/{resource_type}')

    if operation == 'list':
        url = f"{api_base}{endpoint}"
        result = make_request(url, auth=(username, password))
        if result['status'] == 200:
            module.exit_json(changed=False, data=result['data'])
        else:
            module.fail_json(msg=f"Failed to list {resource_type}: {result.get('error', 'Unknown error')}")

    elif operation == 'get':
        url = f"{api_base}{endpoint}"
        result = make_request(url, auth=(username, password))
        if result['status'] == 200:
            items = result['data'] if isinstance(result['data'], list) else [result['data']]
            found = [i for i in items if i.get('name') == name or i.get('userId') == name or i.get('roleId') == name]
            if found:
                module.exit_json(changed=False, data=found[0])
            else:
                module.exit_json(changed=False, data={}, msg=f"{resource_type} '{name}' not found")
        else:
            module.fail_json(msg=f"Failed to get {resource_type}: {result.get('error', 'Unknown error')}")

    elif operation == 'create':
        if state == 'absent':
            module.exit_json(changed=False, msg=f"Nothing to do for state=absent with operation=create")

        # Check if exists
        url = f"{api_base}{endpoint}"
        result = make_request(url, auth=(username, password))
        if result['status'] == 200:
            items = result['data'] if isinstance(result['data'], list) else [result['data']]
            found = [i for i in items if i.get('name') == name]
            if found:
                module.exit_json(changed=False, data=found[0], msg=f"{resource_type} '{name}' already exists")

        # Create
        create_url = f"{api_base}{endpoint}"
        result = make_request(create_url, method='POST', data=body, auth=(username, password))
        if result['status'] in [200, 201]:
            module.exit_json(changed=True, data=result['data'], msg=f"{resource_type} '{name}' created")
        else:
            module.fail_json(msg=f"Failed to create {resource_type}: {result.get('error', 'Unknown error')}")

    elif operation == 'update':
        if state == 'absent':
            module.exit_json(changed=False, msg=f"Nothing to do for state=absent with operation=update")

        update_url = f"{api_base}{endpoint}/{name}"
        result = make_request(update_url, method='PUT', data=body, auth=(username, password))
        if result['status'] in [200, 204]:
            module.exit_json(changed=True, data=result['data'], msg=f"{resource_type} '{name}' updated")
        else:
            module.fail_json(msg=f"Failed to update {resource_type}: {result.get('error', 'Unknown error')}")

    elif operation == 'delete':
        delete_url = f"{api_base}{endpoint}/{name}"
        result = make_request(delete_url, method='DELETE', auth=(username, password))
        if result['status'] in [200, 204]:
            module.exit_json(changed=True, msg=f"{resource_type} '{name}' deleted")
        else:
            module.fail_json(msg=f"Failed to delete {resource_type}: {result.get('error', 'Unknown error')}")


if __name__ == '__main__':
    main()
