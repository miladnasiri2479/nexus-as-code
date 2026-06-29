# nexus_blobstores

Create and manage Nexus Repository Manager blob stores.

## Description

This role creates and manages blob stores via the Nexus REST API.
Supports file (local filesystem) and S3 storage backends.

## Requirements

- Nexus Repository Manager must be installed and running
- Admin credentials must be set

## Role Variables

### Required

| Variable | Description | Default |
|---|---|---|
| `nexus_admin_password` | Admin password | `""` |
| `nexus_blobstores` | List of blob stores | `[]` |

### Blob Store Structure

```yaml
nexus_blobstores:
  - name: default
    type: file
    soft_quota: ""
    file:
      path: /data/nexus

  - name: s3-storage
    type: s3
    soft_quota: 1TB
    s3:
      region: us-east-1
      bucket: my-bucket
      access_key_id: "{{ vault_s3_key }}"
      secret_access_key: "{{ vault_s3_secret }}"
      endpoint: ""
      path_style_access: false
```

### Optional

| Variable | Description | Default |
|---|---|---|
| `nexus_blobstores_delete_unmanaged` | Delete unmanaged blobstores | `false` |
| `nexus_blobstore_valid_types` | Valid blobstore types | `[file, s3]` |
| `nexus_blobstores_run_once` | Run once in multi-host | `false` |
| `nexus_blobstores_delegate_to` | Delegate to host | `""` |
| `nexus_api_retries` | API retry count | `3` |
| `nexus_api_retry_delay` | Retry delay (seconds) | `5` |

## Dependencies

None

## Example Playbook

```yaml
- hosts: nexus
  roles:
    - role: nexus_blobstores
      vars:
        nexus_admin_password: "{{ vault_nexus_admin_password }}"
        nexus_blobstores:
          - name: default
            type: file
            file:
              path: /data/nexus
          - name: docker-blobs
            type: s3
            s3:
              region: us-east-1
              bucket: nexus-docker
              access_key_id: "{{ vault_s3_key }}"
              secret_access_key: "{{ vault_s3_secret }}"
```

## Tags

| Tag | Description |
|---|---|
| `nexus` | All Nexus tasks |
| `blobstores` | All blobstore tasks |
| `validate` | Validation tasks |
| `query` | Query existing blobstores |
| `create` | Create blobstores |
| `verify` | Verify blobstore creation |
| `summary` | Summary output |

## License

Apache-2.0

## Author

nexus-as-code
