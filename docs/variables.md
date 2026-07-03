# Variable Reference

Complete reference for all configuration variables.

## Table of Contents

- [General](#general)
- [Service](#service)
- [JVM](#jvm)
- [Directories](#directories)
- [Storage](#storage)
- [Blob Stores](#blob-stores)
- [Repositories](#repositories)
- [Repository Groups](#repository-groups)
- [Cleanup Policies](#cleanup-policies)
- [Security](#security)
- [Users](#users)
- [Roles](#roles)
- [LDAP](#ldap)
- [TLS](#tls)
- [Proxy](#proxy)
- [SMTP](#smtp)
- [Logging](#logging)
- [Backup](#backup)
- [Restore](#restore)
- [Upgrade](#upgrade)
- [Validation](#validation)
- [MinIO](#minio)
- [Docker](#docker)
- [System](#system)

---

## General

| Variable | Type | Default | Description |
|---|---|---|---|
| `nexus_enabled` | bool | `true` | Enable/disable deployment |
| `nexus_version` | string | `3.72.0` | Nexus version |
| `nexus_edition` | string | `oss` | Edition: `oss` or `pro` |
| `nexus_install_method` | string | `binary` | Method: `binary` or `docker` |
| `nexus_download_url` | string | `""` | Override download URL |
| `nexus_download_checksum` | string | `""` | SHA256 checksum |
| `nexus_download_timeout` | int | `600` | Download timeout (seconds) |

## Service

| Variable | Type | Default | Description |
|---|---|---|---|
| `nexus_service_name` | string | `nexus` | Systemd service name |
| `nexus_service_state` | string | `started` | Desired state |
| `nexus_service_enabled` | bool | `true` | Enable on boot |
| `nexus_port` | int | `8081` | HTTP port |
| `nexus_listen_address` | string | `0.0.0.0` | Bind address |

## JVM

| Variable | Type | Default | Description |
|---|---|---|---|
| `nexus_jvm_memory` | string | `-Xms2703m -Xmx2703m` | Heap memory |
| `nexus_jvm_additional` | string | `""` | Additional JVM flags |
| `nexus_extra_jvm_opts` | string | `""` | Extra options |
| `nexus_max_direct_memory` | string | `2703m` | Direct memory limit |

## Directories

| Variable | Type | Default | Description |
|---|---|---|---|
| `nexus_install_dir` | string | `/opt/sonatype` | Installation root |
| `nexus_data_dir` | string | `/var/nexus/data` | Data directory |
| `nexus_temp_dir` | string | `/var/nexus/tmp` | Temp directory |
| `nexus_work_dir` | string | `/var/nexus/scratch` | Work directory |
| `nexus_runas_user` | string | `nexus` | Service user |
| `nexus_runas_group` | string | `nexus` | Service group |

## Storage

| Variable | Type | Default | Description |
|---|---|---|---|
| `nexus_storage_type` | string | `file` | Backend: `file` or `s3` |
| `nexus_storage_local.path` | string | `/data/nexus` | Local path |
| `nexus_storage_s3.enabled` | bool | `false` | Enable S3 |
| `nexus_storage_s3.region` | string | `us-east-1` | AWS region |
| `nexus_storage_s3.bucket_prefix` | string | `nexus` | Bucket prefix |
| `nexus_storage_s3.access_key_id` | string | `""` | S3 access key |
| `nexus_storage_s3.secret_access_key` | string | `""` | S3 secret key |
| `nexus_storage_s3.endpoint` | string | `""` | S3 endpoint |
| `nexus_storage_s3.path_style_access` | bool | `false` | Path-style URLs |

## Blob Stores

| Variable | Type | Default | Description |
|---|---|---|---|
| `nexus_blobstores` | list | `[]` | List of blob stores |
| `nexus_blobstores[].name` | string | required | Blob store name |
| `nexus_blobstores[].type` | string | `file` | Type: `file` or `s3` |
| `nexus_blobstores[].soft_quota` | string | `""` | Soft quota |

## Repositories

| Variable | Type | Default | Description |
|---|---|---|---|
| `nexus_repos` | list | `[]` | List of repositories |
| `nexus_repos[].name` | string | required | Repository name |
| `nexus_repos[].format` | string | required | Format (maven2, docker, etc.) |
| `nexus_repos[].type` | string | required | Type: hosted, proxy, virtual |
| `nexus_repos[].blob_store_name` | string | `default` | Target blob store |
| `nexus_repos[].write_policy` | string | `""` | Write policy |
| `nexus_repos[].remote_url` | string | `""` | Remote URL (proxy only) |
| `nexus_repos_delete_unmanaged` | bool | `false` | Delete unmanaged repos |

## Repository Groups

| Variable | Type | Default | Description |
|---|---|---|---|
| `nexus_repo_groups` | list | `[]` | List of groups |
| `nexus_repo_groups[].name` | string | required | Group name |
| `nexus_repo_groups[].format` | string | required | Format |
| `nexus_repo_groups[].member_repos` | list | `[]` | Member repos |

## Cleanup Policies

| Variable | Type | Default | Description |
|---|---|---|---|
| `nexus_cleanup_policies` | list | `[]` | List of policies |
| `nexus_cleanup_policies[].name` | string | required | Policy name |
| `nexus_cleanup_policies[].format` | string | required | Format |
| `nexus_cleanup_policies[].repo` | string | required | Target repo |
| `nexus_cleanup_policies[].age` | int | `30` | Retention age |
| `nexus_cleanup_policies[].age_unit` | string | `days` | Age unit |
| `nexus_cleanup_policies[].cron` | string | `""` | Cron schedule |

## Security

| Variable | Type | Default | Description |
|---|---|---|---|
| `nexus_admin_user` | string | `admin` | Admin username |
| `nexus_admin_password` | string | `""` | Admin password |
| `nexus_anonymous_access_enabled` | bool | `false` | Anonymous access |
| `nexus_realms` | list | `[NexusAuthenticatingRealm, NexusAuthoringRealm]` | Active realms |

## Users

| Variable | Type | Default | Description |
|---|---|---|---|
| `nexus_users` | list | `[]` | List of users |
| `nexus_users[].userId` | string | required | User ID |
| `nexus_users[].password` | string | required | Password |
| `nexus_users[].roles` | list | `[]` | Assigned roles |

## Roles

| Variable | Type | Default | Description |
|---|---|---|---|
| `nexus_roles` | list | `[]` | List of roles |
| `nexus_roles[].roleId` | string | required | Role ID |
| `nexus_roles[].name` | string | required | Display name |
| `nexus_roles[].privileges` | list | `[]` | Assigned privileges |

## LDAP

| Variable | Type | Default | Description |
|---|---|---|---|
| `nexus_ldap_enabled` | bool | `false` | Enable LDAP |
| `nexus_ldap.host` | string | `""` | LDAP server |
| `nexus_ldap.port` | int | `389` | LDAP port |
| `nexus_ldap.base_dn` | string | `""` | Base DN |
| `nexus_ldap.bind_dn` | string | `""` | Bind DN |
| `nexus_ldap.bind_password` | string | `""` | Bind password |

## Proxy

| Variable | Type | Default | Description |
|---|---|---|---|
| `nexus_proxy_enabled` | bool | `false` | Enable proxy |
| `nexus_http_proxy_host` | string | `""` | HTTP proxy host |
| `nexus_http_proxy_port` | int | `80` | HTTP proxy port |
| `nexus_no_proxy_hosts` | string | `localhost,127.0.0.1,...` | Bypass hosts |

## Backup

| Variable | Type | Default | Description |
|---|---|---|---|
| `nexus_backup_enabled` | bool | `false` | Enable backup |
| `nexus_backup_dir` | string | `/var/nexus/backup` | Backup directory |
| `nexus_backup_retention_days` | int | `30` | Retention days |
| `nexus_backup_cron_enabled` | bool | `false` | Enable cron |
| `nexus_backup_cron_schedule` | string | `0 2 * * *` | Cron schedule |
| `nexus_backup_s3_enabled` | bool | `false` | Upload to S3 |
| `nexus_backup_s3_bucket` | string | `""` | S3 bucket |

## MinIO

| Variable | Type | Default | Description |
|---|---|---|---|
| `nexus_storage_minio.enabled` | bool | `false` | Enable MinIO |
| `nexus_minio_port` | int | `9000` | API port |
| `nexus_minio_console_port` | int | `9001` | Console port |
| `nexus_minio_access_key` | string | `""` | Access key |
| `nexus_minio_secret_key` | string | `""` | Secret key |
