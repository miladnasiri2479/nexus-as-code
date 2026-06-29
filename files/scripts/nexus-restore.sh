#!/bin/bash
# Nexus Repository Manager Restore Script (Standalone)
# Usage: nexus-restore.sh <backup-file.tar.gz>
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <backup-file.tar.gz>"
    exit 1
fi

BACKUP_FILE="$1"
DATA_DIR="/var/nexus/data"

echo "[$(date)] Restoring from: ${BACKUP_FILE}"

sha256sum -c "${BACKUP_FILE}.sha256" || { echo "Checksum failed"; exit 1; }

systemctl stop nexus || true

RESTORE_DIR=$(mktemp -d)
tar -xzf "${BACKUP_FILE}" -C "${RESTORE_DIR}"
RESTORE_NAME=$(tar -tzf "${BACKUP_FILE}" | head -1 | cut -d'/' -f1)

rm -rf "${DATA_DIR}/orient" "${DATA_DIR}/etc"
cp -a "${RESTORE_DIR}/${RESTORE_NAME}/orient" "${DATA_DIR}/" 2>/dev/null || true
cp -a "${RESTORE_DIR}/${RESTORE_NAME}/etc" "${DATA_DIR}/" 2>/dev/null || true
rsync -a "${RESTORE_DIR}/${RESTORE_NAME}/blobs" "${DATA_DIR}/" 2>/dev/null || true

chown -R nexus:nexus "${DATA_DIR}"
rm -rf "${RESTORE_DIR}"

systemctl start nexus

echo "[$(date)] Restore completed"
