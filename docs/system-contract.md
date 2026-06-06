# Nexus as Code - System Contract

## 1. ASCII Architecture Diagram

```text
                           [ USER CONFIGURATION ]
                           (group_vars/all.yml)
                                     |
                                     v
+-------------------------------------------------------------------------+
|                          ANSIBLE ORCHESTRATOR                           |
|                                                                         |
|  [PHASE 1: INFRASTRUCTURE]                                              |
|  +-------------+       +--------------+           +------------------+  |
|  |  preflight  | ----> | nexus_deploy | --------> |     traefik      |  |
|  +-------------+       +--------------+           +------------------+  |
|         |                      |                            |           |
|         v                      v                            v           |
|   (OS/Packages)          (Docker Vol)                (Docker Net)       |
|                                |                                        |
|  [PHASE 2: API CONFIGURATION]  |                                        |
|                                v                                        |
|                      +-----------------+                                |
|                      | nexus_bootstrap |                                |
|                      +-----------------+                                |
|                                |                                        |
|                                v                                        |
|                      +-----------------+                                |
|                      | nexus_blobstores|                                |
|                      +-----------------+                                |
|                                |                                        |
|                                v                                        |
|                      +------------------+                               |
|                      |nexus_repositories|                               |
|                      +------------------+                               |
+-------------------------------------------------------------------------+
```

## 2. Execution Flow DAG (Directed Acyclic Graph)

The DAG defines strict temporal dependencies. A node cannot execute until its parent successfully completes.

```text
preflight
├── traefik (Independent after preflight, handles edge routing)
└── nexus_deploy (Provisions internal service)
    └── nexus_bootstrap (Requires API to be UP, sets credentials)
        └── nexus_blobstores (Requires Admin Auth, provisions storage)
            └── nexus_repositories (Requires Blobstores to exist, creates logical repos)
```

## 3. Execution Order

To guarantee idempotency and avoid race conditions, execution MUST follow this strict sequence:
1. `preflight`: Prepares host, ensures Docker engine is running.
2. `nexus_deploy`: Boots Nexus container, maps volumes, blocks until API HTTP 200.
3. `traefik`: (Optional) Boots edge proxy, connects to Nexus docker network.
4. `nexus_bootstrap`: Asserts admin credentials, patches anonymous access and security realms.
5. `nexus_blobstores`: Validates and creates physical storage endpoints (Local/S3).
6. `nexus_repositories`: Creates logical repositories bound to the created blobstores.

## 4. State Model (Desired vs Actual State)

- **Desired State**: Strictly defined in `inventories/production/group_vars/all.yml`. No implicit state exists.
- **Actual State**: 
  - Phase 1 (Infra): Docker daemon queries (`docker ps`, `docker network`).
  - Phase 2 (API): Nexus REST API `GET` requests (e.g., `GET /service/rest/v1/blobstores`).
- **Reconciliation**: Roles pull Actual State, diff against Desired State in memory, and issue mutative API calls (`POST`/`PUT`) ONLY if a drift is detected.

## 5. Failure Handling Rules

- **Fail-Fast**: If a desired state schema is invalid (e.g., missing mandatory S3 keys), the pipeline halts *before* making any mutations.
- **API Polling Backoff**: When waiting for Nexus to boot (`nexus_deploy`), poll `/service/rest/v1/status`. Retry up to 30 times with a 10s delay. Halt and fail if timeout occurs.
- **Graceful Auth Degradation**: In `nexus_bootstrap`, the role expects either a `200` (password already changed) or a `401/403` (using default credentials). It dynamically resolves the path without failing.
- **Secrets Masking**: Any task handling passwords, S3 keys, or TLS certs MUST implement `no_log: true` to prevent CI pipeline leakage.

## 6. Contract Rules and Input/Output Schema Per Role

### 6.1 `preflight`
- **Contract**: Ensure host is ready for container orchestration.
- **Inputs**: `ansible_os_family`.
- **Outputs**: Docker service `running`, Python docker SDK installed.
- **Idempotency**: Package managers and Systemd modules handle this natively.

### 6.2 `nexus_deploy`
- **Contract**: Ensure Nexus container is running and healthy.
- **Inputs**: `nexus.version`, `nexus.data_dir`, `nexus.http_port`, `nexus.network_name`.
- **Outputs**: Nexus API responsive on `http_port`.
- **Idempotency**: Docker container recreation only triggers if image tag or mounts change.

### 6.3 `nexus_bootstrap`
- **Contract**: Secure the instance and configure baseline API capabilities.
- **Inputs**: `nexus.admin_password`, `nexus.anonymous_access`.
- **Outputs**: Admin password changed, Docker realm enabled.
- **Idempotency**: Attempts API call with *desired* password first. If it succeeds, the task skips reading the `admin.password` file.

### 6.4 `nexus_blobstores`
- **Contract**: Ensure underlying storage exists before repositories claim them.
- **Inputs**: `blobstores` (List of dicts: file/s3 types).
- **Outputs**: Validated Blobstores in Nexus.
- **Idempotency**: Fetches current blobstores. Uses `POST` for missing, `PUT` for existing.

### 6.5 `nexus_repositories`
- **Contract**: Bind logical catalogs to physical blobstores.
- **Inputs**: `repositories` (Dict with `enabled` toggles and `blobstore` overrides), `repo_catalog` (Internal schema).
- **Outputs**: Accessible proxy/hosted endpoints.
- **Idempotency**: Skips any repo where `enabled: false`. Fetches current repos; applies `POST`/`PUT` safely.

### 6.6 `traefik`
- **Contract**: Secure external edge access.
- **Inputs**: `traefik.domain`, `traefik.letsencrypt`, `traefik.email`.
- **Outputs**: Port 80/443 bound, TLS certificates provisioned.
- **Idempotency**: Dynamic file provider ensures Traefik updates routing instantly without container restarts.
