# nexus_repos_groups

Create and manage Nexus Repository Manager repository groups.

## Description

This role creates, updates, and manages repository groups via the Nexus REST API.
Groups aggregate multiple repositories under a single virtual endpoint.

## Requirements

- Nexus Repository Manager must be installed and running
- Admin credentials must be set
- Member repositories must exist before creating groups

## Role Variables

### Required

| Variable | Description | Default |
|---|---|---|
| `nexus_admin_password` | Admin password | `""` |
| `nexus_repo_groups` | List of repository groups | `[]` |

### Group Structure

```yaml
nexus_repo_groups:
  - name: maven-public
    format: maven2
    blob_store_name: default
    strict_content_validation: true
    member_repos:
      - maven-releases
      - maven-snapshots
      - maven-central
```

### Optional

| Variable | Description | Default |
|---|---|---|
| `nexus_repo_groups_delete_unmanaged` | Delete unmanaged groups | `false` |
| `nexus_repo_group_valid_formats` | Valid group formats | `[maven2, docker, ...]` |
| `nexus_repo_groups_run_once` | Run once in multi-host | `false` |
| `nexus_repo_groups_delegate_to` | Delegate to host | `""` |
| `nexus_api_retries` | API retry count | `3` |
| `nexus_api_retry_delay` | Retry delay (seconds) | `5` |

## Dependencies

None (but member repositories should exist first)

## Example Playbook

```yaml
- hosts: nexus
  roles:
    - role: nexus_repos_groups
      vars:
        nexus_admin_password: "{{ vault_nexus_admin_password }}"
        nexus_repo_groups:
          - name: maven-public
            format: maven2
            member_repos:
              - maven-releases
              - maven-snapshots
              - maven-central
          - name: docker-group
            format: docker
            member_repos:
              - docker-hosted
              - docker-hub
```

## Tags

| Tag | Description |
|---|---|
| `nexus` | All Nexus tasks |
| `repo-groups` | All group tasks |
| `validate` | Validation tasks |
| `query` | Query existing groups |
| `create` | Create groups |
| `update` | Update groups |
| `delete` | Delete groups |
| `summary` | Summary output |

## License

Apache-2.0

## Author

nexus-as-code
