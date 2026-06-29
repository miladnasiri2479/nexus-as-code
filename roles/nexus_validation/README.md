# nexus_validation

Validate Nexus Repository Manager configuration before deployment.

## Purpose

This role performs comprehensive pre-flight checks on your Nexus configuration
to catch errors before they cause deployment failures. It validates variable
consistency, references, credentials, and format compliance.

## Usage

```yaml
# In your playbook (automatic — included in nexus_deploy.yml):
- role: nexus_validation

# Standalone validation:
ansible-playbook -i inventories/production/inventory.yml playbooks/nexus_validate.yml

# Skip validation in deploy playbook:
ansible-playbook -i inventories/production/inventory.yml playbooks/nexus_deploy.yml \
  --skip-tags validation

# Run only validation:
ansible-playbook -i inventories/production/inventory.yml playbooks/nexus_deploy.yml \
  --tags validation
```

## Checks Performed

### Duplicate Detection

| Check | Error Code | Description |
|---|---|---|
| Duplicate repos | `DUPLICATE_REPOSITORY` | Same `name` defined twice in `nexus_repos` |
| Duplicate blobstores | `DUPLICATE_BLOBSTORE` | Same `name` defined twice in `nexus_blobstores` |
| Duplicate buckets | `DUPLICATE_BUCKET` | Same `name` defined twice in `nexus_minio_buckets` |
| Duplicate ports | `DUPLICATE_PORT` | Same port assigned to multiple services |

### Credential Validation

| Check | Error Code | Description |
|---|---|---|
| Admin password | `MISSING_CREDENTIAL` | `nexus_admin_password` is empty |
| S3 credentials | `MISSING_CREDENTIAL` | S3 enabled but `access_key_id` or `secret_access_key` missing |
| MinIO credentials | `MISSING_CREDENTIAL` | MinIO enabled but keys missing |
| LDAP credentials | `MISSING_CREDENTIAL` | LDAP enabled but `bind_dn` or `bind_password` missing |
| Proxy credentials | `MISSING_CREDENTIAL` | Proxy enabled with auth but credentials missing |

### Mapping Validation

| Check | Error Code | Description |
|---|---|---|
| Blobstore mapping | `INVALID_MAPPING` | Repo references blob store not in `nexus_blobstores` |
| Cleanup mapping | `INVALID_MAPPING` | Policy references repo not in `nexus_repos` |
| Group members | `INVALID_MAPPING` | Group member not in `nexus_repos` |
| Privilege format | `INVALID_PRIVILEGE` | Privilege name doesn't match `nx-repository-view-*-*-*` |

### Storage Validation

| Check | Error Code | Description |
|---|---|---|
| File storage path | `INVALID_STORAGE` | `type: file` but `nexus_storage.file.path` empty |
| S3 endpoint | `INVALID_STORAGE` | `type: s3` but `nexus_storage.s3.endpoint` empty |
| MinIO port | `INVALID_STORAGE` | MinIO enabled but port not set |

### Proxy Validation

| Check | Error Code | Description |
|---|---|---|
| Proxy host | `MISSING_PROXY_VALUE` | Proxy enabled but host empty |
| Proxy port | `INVALID_PROXY` | Port out of range (1-65535) |
| No-proxy hosts | `MISSING_PROXY_VALUE` | `nexus_no_proxy_hosts` empty |

### Format Validation

| Check | Error Code | Description |
|---|---|---|
| Repo formats | `UNSUPPORTED_FORMAT` | Format not in supported list |
| Storage types | `UNSUPPORTED_STORAGE` | Storage type not in `file`, `s3` |

### Cleanup Policy Validation

| Check | Error Code | Description |
|---|---|---|
| Policy age | `INVALID_CLEANUP` | Age < 1 |
| Cron expression | `INVALID_CLEANUP` | Not 6 fields (Quartz format) |
| Age unit | `INVALID_CLEANUP` | Not in `minutes`, `hours`, `days`, `weeks`, `months` |

### Cross-Checks

| Check | Error Code | Description |
|---|---|---|
| Empty repo name | `INVALID_REPO` | Repository `name` is empty string |
| Missing format | `INVALID_REPO` | Repository missing required `format` field |
| Missing remote_url | `INVALID_REPO` | Proxy repo missing `remote_url` |
| Empty group | `EMPTY_GROUP` | Group has no `member_repos` |

## Configuration

### Enable/Disable Checks

```yaml
# Disable specific checks:
nexus_validation_check_duplicate_repos: false
nexus_validation_check_s3_credentials: false

# Disable all pre-flight checks:
nexus_validation_preflight: false

# Warn only (don't fail on errors):
nexus_validation_fail_on_error: false
```

### Output Example

```
========================================
  NEXUS CONFIGURATION VALIDATION REPORT
========================================

Errors:   2
Warnings: 1

ERROR: MISSING_CREDENTIAL: nexus_admin_password is empty. You must set the Nexus admin password...
ERROR: DUPLICATE_REPOSITORY: The following repository names are defined more than once: maven-releases...
WARNING: EMPTY_GROUP: The following repository groups have no member repositories: custom-group...
```

## Variables

See `defaults/main.yml` for all configuration variables with descriptions.

## Dependencies

None — this role has no dependencies and can run standalone.

## Tags

```
validation, duplicates, credentials, mappings, storage, proxy,
formats, cleanup, ports, cross-checks
```

Run only validation:
```bash
ansible-playbook ... --tags validation
```

Run only credential checks:
```bash
ansible-playbook ... --tags validation,credentials
```
