# Backup Guide

## Overview

The backup system creates compressed archives of Nexus data, configuration, and blob stores.

## What Gets Backed Up

| Component | Path | Default |
|---|---|---|
| Database | `{data_dir}/orient` | ✅ |
| Configuration | `{data_dir}/etc` | ✅ |
| Blob Stores | `{data_dir}/blobs` | ✅ |

## Configuration

```yaml
nexus_backup_enabled: true

# Directory
nexus_backup_dir: /var/nexus/backup
nexus_backup_temp_dir: /tmp/nexus-backup

# What to include
nexus_backup_include_blobs: true
nexus_backup_include_db: true
nexus_backup_include_config: true

# Compression
nexus_backup_compress: true

# Retention
nexus_backup_retention_days: 30
nexus_backup_retention_count: 10

# Cron schedule
nexus_backup_cron_enabled: true
nexus_backup_cron_schedule: "0 2 * * *"

# S3 upload
nexus_backup_s3_enabled: true
nexus_backup_s3_bucket: my-nexus-backups
nexus_backup_s3_prefix: backups
nexus_backup_s3_endpoint: ""
```

## Running Backup

```bash
# Via playbook
ansible-playbook -i inventories/production/inventory.yml playbooks/nexus_backup.yml

# Via script (on the server)
/usr/local/bin/nexus-backup.sh --retention 30
```

## Backup Output

```
/var/nexus/backup/
├── nexus-backup-20240115_020000.tar.gz
├── nexus-backup-20240115_020000.tar.gz.sha256
├── nexus-backup-20240114_020000.tar.gz
├── nexus-backup-20240114_020000.tar.gz.sha256
└── ...
```

## S3 Backup

```yaml
nexus_backup_s3_enabled: true
nexus_backup_s3_bucket: my-nexus-backups
nexus_backup_s3_prefix: production
nexus_backup_s3_endpoint: "https://s3.amazonaws.com"
```

Backups are uploaded to:
```
s3://my-nexus-backups/production/nexus-backup-20240115_020000.tar.gz
s3://my-nexus-backups/production/nexus-backup-20240115_020000.tar.gz.sha256
```

## Notification

```yaml
nexus_backup_notify_enabled: true
nexus_backup_notify_email: admin@example.com
nexus_backup_notify_webhook: https://hooks.slack.com/services/xxx
```
