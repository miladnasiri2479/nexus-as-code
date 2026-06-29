#!/bin/bash
# Nexus Repository Manager Backup Script (Standalone)
# Usage: nexus-backup.sh [--retention DAYS]
set -euo pipefail

BACKUP_DIR="/var/nexus/backup"
DATA_DIR="/var/nexus/data"
RETENTION_DAYS=30

while [[ $# -gt 0 ]]; do
    case $1 in
        --retention) RETENTION_DAYS="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="nexus-backup-${TIMESTAMP}"

mkdir -p "${BACKUP_DIR}"

echo "[$(date)] Starting backup: ${BACKUP_NAME}"

tar -czf "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" \
    -C "$(dirname ${DATA_DIR})" \
    "$(basename ${DATA_DIR})" 2>/dev/null || true

sha256sum "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" > "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz.sha256"

find "${BACKUP_DIR}" -name "nexus-backup-*.tar*" -mtime +${RETENTION_DAYS} -delete 2>/dev/null || true

echo "[$(date)] Backup completed: ${BACKUP_NAME}"
