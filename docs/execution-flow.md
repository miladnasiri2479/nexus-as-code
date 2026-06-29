# Execution Flow

## Overview

This document describes the execution flow for each playbook.

## Full Deployment (`nexus_deploy.yml`)

```mermaid
graph TD
    Start([Start]) --> Validate[Validate Config]
    Validate --> Common[OS Preparation]
    Common --> Java[Install Java]
    Java --> Storage{Storage Type?}
    Storage -->|file| Local[Configure Local Storage]
    Storage -->|s3| S3[Configure S3 Storage]
    Local --> MinIO{MinIO Enabled?}
    S3 --> MinIO
    MinIO -->|yes| MinIOSetup[Install MinIO]
    MinIO -->|no| Install[Nexus Install]
    MinIOSetup --> Buckets[Create Buckets]
    Buckets --> Install
    Install --> Config[Configure Nexus]
    Config --> Blobstores[Create Blobstores]
    Blobstores --> Repos[Create Repositories]
    Repos --> Groups[Create Repository Groups]
    Groups --> Cleanup[Create Cleanup Policies]
    Cleanup --> Security[Configure Security]
    Security --> LDAP{LDAP Enabled?}
    LDAP -->|yes| LDAPSetup[Configure LDAP]
    LDAP -->|no| Proxy{Proxy Enabled?}
    LDAPSetup --> Proxy
    Proxy -->|yes| ProxySetup[Configure Proxy]
    Proxy -->|no| Validate2[Validate Deployment]
    ProxySetup --> Validate2
    Validate2 --> Done([Complete])

    style Start fill:#e1f5fe
    style Done fill:#c8e6c9
    style Install fill:#fff3e0
    style Security fill:#fce4ec
```

### Task Sequence

| Step | Role | Tasks | Duration |
|---|---|---|---|
| 1 | common | Install packages, create user, dirs, sysctl | ~30s |
| 2 | java | Install OpenJDK 17 | ~60s |
| 3 | storage | Configure storage backend | ~5s |
| 4 | minio | Install MinIO (if enabled) | ~60s |
| 5 | storage_bucket_create | Create buckets (if enabled) | ~10s |
| 6 | nexus_install | Download, extract, systemd, start | ~120s |
| 7 | nexus_config | Write properties, JVM, logging | ~10s |
| 8 | nexus_blobstores | Create blob stores | ~15s |
| 9 | nexus_repos | Create repositories | ~30s |
| 10 | nexus_repos_groups | Create groups | ~10s |
| 11 | nexus_cleanup | Create cleanup policies | ~10s |
| 12 | nexus_security | Configure users, roles, realms | ~15s |
| 13 | nexus_ldap | Configure LDAP (if enabled) | ~10s |
| 14 | nexus_proxy | Configure proxy (if enabled) | ~5s |
| 15 | nexus_verification | Verify deployment | ~20s |
| **Total** | | | **~5-10 min** |

## Install Only (`nexus_install.yml`)

```mermaid
graph TD
    Start --> Common[OS Preparation]
    Common --> Java[Install Java]
    Java --> Install[Nexus Install]
    Install --> Done([Complete])
```

## Configure Only (`nexus_configure.yml`)

```mermaid
graph TD
    Start --> Config[Configure Nexus]
    Config --> Blobstores[Create Blobstores]
    Blobstores --> Repos[Create Repositories]
    Repos --> Groups[Create Groups]
    Groups --> Cleanup[Create Cleanup Policies]
    Cleanup --> Security[Configure Security]
    Security --> Proxy{Proxy Enabled?}
    Proxy -->|yes| ProxySetup[Configure Proxy]
    Proxy -->|no| Done([Complete])
    ProxySetup --> Done
```

## Backup (`nexus_backup.yml`)

```mermaid
graph TD
    Start --> Validate{Backup Enabled?}
    Validate -->|no| Skip([Skip])
    Validate -->|yes| CreateDir[Create Backup Directory]
    CreateDir --> Scripts[Write Backup Scripts]
    Scripts --> Cron[Configure Cron Job]
    Cron --> Logrotate[Configure Log Rotation]
    Logrotate --> Done([Complete])
```

## Restore (`nexus_restore.yml`)

```mermaid
graph TD
    Start --> Validate[Validate Source]
    Validate --> Checksum[Verify Checksum]
    Checksum --> Stop[Stop Nexus]
    Stop --> Snapshot[Create Pre-restore Snapshot]
    Snapshot --> Extract[Extract Backup]
    Extract --> RestoreDB[Restore Database]
    RestoreDB --> RestoreConfig[Restore Configuration]
    RestoreConfig --> RestoreBlobs[Restore Blob Stores]
    RestoreBlobs --> Permissions[Set Permissions]
    Permissions --> Start[Start Nexus]
    Start --> WaitAPI[Wait for API]
    WaitAPI --> Done([Complete])
```

## Upgrade (`nexus_upgrade.yml`)

```mermaid
graph TD
    Start --> Detect[Detect Current Version]
    Detect --> Skip{Same Version?}
    Skip -->|yes| SkipMsg([Skip Upgrade])
    Skip -->|no| Backup[Create Backup]
    Backup --> Stop[Stop Service]
    Stop --> Wait[Wait for Stop]
    Wait --> Install[Install New Version]
    Install --> Start[Start Service]
    Start --> WaitAPI[Wait for API]
    WaitAPI --> Verify[Verify Version]
    Verify --> Done([Complete])
```

## Destroy (`nexus_destroy.yml`)

```mermaid
graph TD
    Start --> Confirm{Confirmed?}
    Confirm -->|no| Abort([Abort])
    Confirm -->|yes| Stop[Stop Service]
    Stop --> Docker{Docker?}
    Docker -->|yes| StopContainer[Stop Container]
    Docker -->|no| RemoveFiles[Remove Files]
    StopContainer --> RemoveFiles
    RemoveFiles --> RemoveUser[Remove User]
    RemoveUser --> Reload[Reload Systemd]
    Reload --> Done([Complete])
```

## Validation (`nexus_validate.yml`)

```mermaid
graph TD
    Start --> Dupes[Check Duplicates]
    Dupes --> Creds[Check Credentials]
    Creds --> Maps[Check Mappings]
    Maps --> Storage[Check Storage]
    Storage --> Proxy[Check Proxy]
    Proxy --> Formats[Check Formats]
    Formats --> Cleanup[Check Cleanup Policies]
    Cleanup --> Report[Generate Report]
    Report --> Errors{Errors?}
    Errors -->|yes| Fail([Fail])
    Errors -->|no| Pass([Pass])
```
