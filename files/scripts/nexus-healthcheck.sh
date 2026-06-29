#!/bin/bash
# Nexus Repository Manager Health Check Script (Standalone)
# Usage: nexus-healthcheck.sh
set -euo pipefail

NEXUS_URL="http://localhost:8081"
MAX_RETRIES=5
RETRY_DELAY=10

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

check_api() {
    local status
    status=$(curl -s -o /dev/null -w "%{http_code}" "${NEXUS_URL}/service/rest/v1/status")
    [ "$status" = "200" ]
}

RETRIES=0
until check_api; do
    RETRIES=$((RETRIES + 1))
    if [ "$RETRIES" -ge "$MAX_RETRIES" ]; then
        log "ERROR: Nexus API not responding"
        exit 1
    fi
    log "Waiting... (attempt ${RETRIES}/${MAX_RETRIES})"
    sleep "$RETRY_DELAY"
done

log "Nexus health check: OK"
