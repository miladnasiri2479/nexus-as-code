# nexus_repos

Create and manage Nexus Repository Manager repositories.

## Description

This role creates, updates, and manages repositories via the Nexus REST API.
Supports all formats: Maven, Docker, npm, PyPI, Helm, Raw, Go, NuGet, YUM, APT, and more.

## Requirements

- Nexus Repository Manager must be installed and running
- Admin credentials must be set
- Blob stores must exist before creating repositories

## Role Variables

### Required

| Variable | Description | Default |
|---|---|---|
| `nexus_admin_password` | Admin password | `""` |
| `nexus_repos` | List of repositories | `[]` |

### Repository Structure

```yaml
nexus_repos:
  - name: maven-releases
    format: maven2
    type: hosted
    write_policy: allow_once
    version_policy: release
    blob_store_name: default
    cleanup_policy: ""
    online: true

  - name: docker-proxy
    format: docker
    type: proxy
    remote_url: https://registry-1.docker.io
    blob_store_name: default
    cache_max_age_in_minutes: 1440
```

### Optional

| Variable | Description | Default |
|---|---|---|
| `nexus_repos_delete_unmanaged` | Delete unmanaged repos | `false` |
| `nexus_repos_expected` | Repos to keep (unmanaged) | `[]` |
| `nexus_repo_blobstore_map` | Explicit repo→blobstore mapping | `{}` |
| `nexus_format_blobstore_defaults` | Default blobstore per format | `{...}` |
| `nexus_repo_valid_formats` | Valid repository formats | `[maven2, docker, ...]` |
| `nexus_repo_valid_types` | Valid repository types | `[hosted, proxy, virtual]` |
| `nexus_repos_run_once` | Run once in multi-host | `false` |
| `nexus_repos_delegate_to` | Delegate to host | `""` |
| `nexus_api_retries` | API retry count | `3` |
| `nexus_api_retry_delay` | Retry delay (seconds) | `5` |

## Dependencies

None (but blob stores should exist first)

## Example Playbook

```yaml
- hosts: nexus
  roles:
    - role: nexus_repos
      vars:
        nexus_admin_password: "{{ vault_nexus_admin_password }}"
        nexus_repos:
          - name: maven-releases
            format: maven2
            type: hosted
            write_policy: allow_once
            version_policy: release
            blob_store_name: default
          - name: docker-hosted
            format: docker
            type: hosted
            write_policy: allow
            http_port: 5000
            blob_store_name: default
          - name: maven-central
            format: maven2
            type: proxy
            remote_url: https://repo1.maven.org/maven2
            blob_store_name: default
```

## Tags

| Tag | Description |
|---|---|
| `nexus` | All Nexus tasks |
| `repos` | All repository tasks |
| `validate` | Validation tasks |
| `query` | Query existing repos |
| `mapping` | Blobstore mapping |
| `create` | Create repositories |
| `update` | Update repositories |
| `delete` | Delete repositories |
| `summary` | Summary output |

## License

Apache-2.0

## Author

nexus-as-code
