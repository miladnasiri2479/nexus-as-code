# Nexus as Code - Implementation Plan

This document translates the `SYSTEM_CONTRACT.md` into a deterministic, step-by-step roadmap for Ansible development.

## Phase 1: Infrastructure Foundation
**Goal:** Provision the host and get the raw Nexus container running.

### 1. `preflight` Role
*   **Variables Consumed:** `ansible_os_family` (Ansible Fact).
*   **APIs Called:** None.
*   **Files Modified:** OS package manager caches (`apt`/`dnf`), Systemd configuration for Docker.
*   **Checklist:**
    - [ ] Assert OS is Debian or RedHat.
    - [ ] Install Docker and Python SDK (`docker.io`, `python3-docker`).
    - [ ] Ensure Docker systemd service is `started` and `enabled`.
*   **Validation:** Docker daemon responds to module commands successfully.

### 2. `nexus_deploy` Role
*   **Variables Consumed:** `nexus.version`, `nexus.data_dir`, `nexus.http_port`, `nexus.network_name`.
*   **APIs Called:** `GET /service/rest/v1/status` (Polling only, to block until ready).
*   **Files Modified:** Creates directory `nexus.data_dir` with owner `200:200`.
*   **Checklist:**
    - [ ] Create Docker network (`nexus.network_name`).
    - [ ] Create local data directory with correct UID/GID.
    - [ ] Deploy Nexus Docker container with `healthcheck`.
    - [ ] Wait for `GET /service/rest/v1/status` to return HTTP 200.
*   **Validation:** Ansible playbook pauses until Nexus API is fully initialized.

> **Integration Checkpoint 1**: At this stage, curling `http://localhost:8081` on the target machine returns the Nexus UI/API.

---

## Phase 2: Edge Proxy
**Goal:** Secure the perimeter and route external traffic.

### 3. `traefik` Role
*   **Variables Consumed:** `traefik.enabled`, `traefik.version`, `traefik.domain`, `traefik.letsencrypt`, `traefik.email`, `traefik.config_dir`, `nexus.network_name`, `nexus.container_name`, `nexus.http_port`.
*   **APIs Called:** None (Uses local Docker socket).
*   **Files Modified:** Creates `/opt/traefik/traefik.yml`, `/opt/traefik/dynamic/nexus.yml`, `/opt/traefik/acme.json` (chmod 0600).
*   **Checklist:**
    - [ ] Create Traefik config directories.
    - [ ] Touch `acme.json` with strict `0600` permissions.
    - [ ] Template static config (`traefik.yml.j2`).
    - [ ] Template dynamic routing config (`dynamic_conf.yml.j2`).
    - [ ] Deploy Traefik Docker container attached to Nexus network.
*   **Validation:** HTTP to HTTPS redirection works; `https://<traefik.domain>` successfully routes to Nexus UI.

> **Integration Checkpoint 2**: Nexus is externally accessible and secured via TLS (if Let's Encrypt is enabled).

---

## Phase 3: API Configuration
**Goal:** Secure the application and setup system realms.

### 4. `nexus_bootstrap` Role
*   **Variables Consumed:** `nexus.admin_password`, `nexus.anonymous_access`, `nexus.data_dir`, `nexus.http_port`.
*   **APIs Called:**
    - `GET /service/rest/v1/security/users?userId=admin`
    - `PUT /service/rest/v1/security/users/admin/change-password`
    - `GET` & `PUT /service/rest/v1/security/anonymous`
    - `GET` & `PUT /service/rest/v1/security/realms/active`
*   **Files Modified:** Reads (does not write) `{{ nexus.data_dir }}/admin.password`.
*   **Checklist:**
    - [ ] Check if `admin_password` works. If 401/403, proceed to read initial password.
    - [ ] Slurp initial password from host disk.
    - [ ] PUT new `admin_password`.
    - [ ] GET anonymous state; PUT new state if drifted from `nexus.anonymous_access`.
    - [ ] GET active realms; PUT `DockerToken` realm if missing.
*   **Validation:** Subsequent API calls using the *new* `nexus.admin_password` succeed (HTTP 200).

> **Integration Checkpoint 3**: Default credentials are removed, and system is ready to accept Docker/Registry traffic.

---

## Phase 4: Storage & Data Bound Logic
**Goal:** Provision Blobstores and Repositories dynamically.

### 5. `nexus_blobstores` Role
*   **Variables Consumed:** `blobstores` (List of dictionaries defining file or S3 configs).
*   **APIs Called:**
    - `GET /service/rest/v1/blobstores`
    - `POST /service/rest/v1/blobstores/{type}`
    - `PUT /service/rest/v1/blobstores/{type}/{name}`
*   **Files Modified:** None (Managed entirely via Nexus).
*   **Checklist:**
    - [ ] GET existing blobstores list.
    - [ ] Loop through `blobstores` variable.
    - [ ] Construct payload (File or S3/MinIO based).
    - [ ] POST payload if blobstore does not exist.
    - [ ] PUT payload if blobstore exists (Idempotent update).
*   **Validation:** Blobstores appear correctly in the Nexus UI under Administration -> Repository -> Blob Stores.

### 6. `nexus_repositories` Role
*   **Variables Consumed:** `repositories` (User dict with enabled flags and blobstore overrides), `repo_catalog` (Internal YAML database).
*   **APIs Called:**
    - `GET /service/rest/v1/repositories`
    - `POST /service/rest/v1/repositories/{format}/{type}`
    - `PUT /service/rest/v1/repositories/{format}/{type}/{name}`
*   **Files Modified:** None.
*   **Checklist:**
    - [ ] Load internal `catalog.yml`.
    - [ ] GET existing repositories list.
    - [ ] Loop over user `repositories`. Skip if `enabled: false`.
    - [ ] Merge internal catalog payload with user blobstore override.
    - [ ] POST payload if repository does not exist.
    - [ ] PUT payload if repository exists (Idempotent update).
*   **Validation:** Running `curl -u admin:<pass> -X GET http://localhost:8081/repository/<name>/` returns 200 OK.

> **Final Integration Checkpoint**: The Nexus infrastructure is 100% compliant with the `all.yml` configuration and ready for user workloads.
