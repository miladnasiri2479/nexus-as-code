# Nexus Backup & Restore Role

Provides optional, automated, and versioned backups of the entire Nexus state (Metadata, Configuration, and Local Blobs). 

## Execution Rule
This role strictly executes **ONLY IF**:
```yaml
features:
  backup:
    enabled: true
```

## Features
- **Versioned Backups**: Generates backups in the format `nexus-backup-YYYYMMDD_HHMMSS.tar.gz`.
- **Destinations**: Supports storing backups strictly `local`, or pushing them to AWS `s3`, or `minio`.
- **Scheduled Trigger**: Deploys a cron job based on the `features.backup.schedule` expression.
- **Manual Trigger**: Can be forced to run immediately via Ansible by setting `run_backup_now: true`.
- **Idempotent Restore**: Contains a dedicated `restore.yml` task file that safely shuts down the container, wipes the corrupted volume, extracts the specific versioned backup, and re-starts the container.

## Configuration

**group_vars/all.yml**
```yaml
features:
  backup:
    enabled: true
    schedule: "0 2 * * *" # Cron format
    retention_days: 7
    destination: "s3"     # file, s3, minio
    bucket: "nexus-backups"
    access_key: "AKIA..."
    secret_key: "SECRET..."
```

## How to trigger a Restore
To trigger an idempotent restore of a specific backup version, pass the `restore_backup_file` variable at runtime:

```bash
ansible-playbook -i inventories/production/hosts.yml playbooks/site.yml \
  --tags "backup" \
  -e "restore_backup_file=nexus-backup-20231027_020000.tar.gz"
```
