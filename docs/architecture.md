# Architecture

## Overview

This project follows the [Kubespray](https://github.com/kubernetes-sigs/kubespray) architecture pattern for Ansible projects. Every component is isolated into its own role, fully data-driven, and configurable from a single inventory file.

## Directory Structure

```
nexus-as-code/
├── ansible.cfg                    # Ansible configuration
├── galaxy.yml                     # Galaxy metadata
├── requirements.yml               # External dependencies
├── .gitignore
├── .yamllint
│
├── group_vars/
│   └── all/
│       └── nexus.yml              # MASTER CONFIGURATION
│
├── inventories/
│   ├── production/
│   │   ├── inventory.yml
│   │   └── group_vars/
│   │       └── nexus.yml          # Environment overrides
│   ├── staging/
│   └── testing/
│
├── roles/                         # 30+ independent roles
│   ├── common/                    # OS prerequisites
│   ├── java/                      # OpenJDK installation
│   ├── nexus_install/             # Nexus installation
│   ├── nexus_config/              # Runtime configuration
│   ├── storage/                   # Storage orchestrator
│   ├── storage_local/             # Local filesystem
│   ├── storage_minio/             # MinIO server
│   ├── storage_s3/                # S3 backend
│   ├── storage_bucket_create/     # Bucket creation
│   ├── storage_bucket_validate/   # Bucket validation
│   ├── nexus_blobstores/          # Blob store management
│   ├── nexus_repos/               # Repository management
│   ├── nexus_repos_groups/        # Repository groups
│   ├── nexus_cleanup/             # Cleanup policies
│   ├── nexus_security/            # Security core
│   ├── nexus_ldap/                # LDAP integration
│   ├── nexus_users/               # User management
│   ├── nexus_roles/               # Role management
│   ├── nexus_privileges/          # Privilege validation
│   ├── nexus_proxy/               # Outbound proxy
│   ├── nexus_backup/              # Backup
│   ├── nexus_restore/             # Restore
│   ├── nexus_upgrade/             # Upgrade
│   ├── nexus_destroy/             # Destruction
│   ├── nexus_healthcheck/         # Health checks
│   ├── nexus_verification/        # Configuration verification
│   └── nexus_validation/          # Pre-flight validation
│
├── playbooks/                     # Orchestration playbooks
├── plugins/                       # Custom modules/filters
├── files/scripts/                 # Helper scripts
└── tests/                         # Molecule tests
```

## Design Principles

### 1. Single Source of Truth

The **only** file users edit is:

```
inventories/<env>/group_vars/nexus.yml
```

All Ansible code reads from this file. No hardcoded values in roles.

### 2. Role Independence

Each role:
- Has its own `defaults/main.yml`
- Reads only from inventory variables
- Can be run independently
- Has no circular dependencies

### 3. Idempotency

Every task is idempotent — running the same playbook multiple times produces the same result without side effects.

### 4. Data-Driven Configuration

```yaml
# Everything is a list or dict — add a repo = add an entry
nexus_repos:
  - name: my-repo
    format: maven2
    type: hosted
```

### 5. Layered Precedence

```
host_vars/<host>.yml           (highest)
  ↓
inventories/<env>/group_vars/nexus.yml
  ↓
group_vars/all/nexus.yml
  ↓
roles/*/defaults/main.yml      (lowest)
```

## Role Dependency Graph

```mermaid
graph TD
    common --> java
    common --> storage_local
    java --> nexus_install
    nexus_install --> nexus_config
    nexus_install --> nexus_blobstores
    nexus_blobstores --> nexus_repos
    nexus_repos --> nexus_repos_groups
    nexus_install --> nexus_cleanup
    nexus_install --> nexus_security
    nexus_security --> nexus_ldap
    nexus_security --> nexus_users
    nexus_users --> nexus_roles
    nexus_roles --> nexus_privileges
    nexus_install --> nexus_proxy
    nexus_install --> nexus_backup
    nexus_backup --> nexus_restore
    nexus_install --> nexus_upgrade
    nexus_install --> nexus_verification
    nexus_install --> nexus_healthcheck
    nexus_install --> nexus_validation
    minio --> minio_bucket
    minio_bucket --> storage_bucket_create
    storage_bucket_create --> storage_bucket_validate

    style common fill:#e1f5fe
    style java fill:#e1f5fe
    style nexus_install fill:#fff3e0
    style nexus_config fill:#fff3e0
    style nexus_blobstores fill:#e8f5e9
    style nexus_repos fill:#e8f5e9
    style nexus_security fill:#fce4ec
    style nexus_backup fill:#f3e5f5
    style minio fill:#e0f2f1
```

## Execution Flow

### Full Deployment

```mermaid
sequenceDiagram
    participant User
    participant Ansible
    participant Common
    participant Java
    participant Install
    participant Config
    participant Blobstores
    participant Repos
    participant Groups
    participant Cleanup
    participant Security
    participant Validation

    User->>Ansible: ansible-playbook nexus_deploy.yml
    Ansible->>Common: Install packages, create user
    Common-->>Ansible: OK
    Ansible->>Java: Install OpenJDK 17
    Java-->>Ansible: OK
    Ansible->>Install: Download, extract, systemd
    Install-->>Ansible: Nexus running on :8081
    Ansible->>Config: Write properties, JVM, logging
    Config-->>Ansible: OK
    Ansible->>Blobstores: Create file/S3 blob stores
    Blobstores-->>Ansible: OK
    Ansible->>Repos: Create repositories
    Repos-->>Ansible: OK
    Ansible->>Groups: Create repository groups
    Groups-->>Ansible: OK
    Ansible->>Cleanup: Create cleanup policies
    Cleanup-->>Ansible: OK
    Ansible->>Security: Configure users, roles, realms
    Security-->>Ansible: OK
    Ansible->>Validation: Verify deployment
    Validation-->>Ansible: PASSED
    Ansible-->>User: Deployment complete
```

### Upgrade Flow

```mermaid
sequenceDiagram
    participant User
    participant Ansible
    participant Upgrade
    participant Backup
    participant Install
    participant Validation

    User->>Ansible: ansible-playbook nexus_upgrade.yml
    Ansible->>Upgrade: Check current version
    Upgrade-->>Ansible: Current: 3.71.0, Target: 3.72.0
    Ansible->>Backup: Create pre-upgrade backup
    Backup-->>Ansible: Backup complete
    Ansible->>Upgrade: Stop service
    Upgrade-->>Ansible: Service stopped
    Ansible->>Install: Install new version
    Install-->>Ansible: 3.72.0 installed
    Ansible->>Upgrade: Start service
    Upgrade-->>Ansible: Service started
    Ansible->>Validation: Verify API health
    Validation-->>Ansible: PASSED
    Ansible-->>User: Upgrade complete
```

### Backup Flow

```mermaid
sequenceDiagram
    participant User
    participant Ansible
    participant Backup
    participant S3
    participant Notification

    User->>Ansible: ansible-playbook nexus_backup.yml
    Ansible->>Backup: Run backup script
    Backup->>Backup: Copy database
    Backup->>Backup: Copy configuration
    Backup->>Backup: Copy blob stores
    Backup->>Backup: Create tar.gz
    Backup->>Backup: Generate checksum
    Backup->>S3: Upload to S3 (if enabled)
    S3-->>Backup: Upload complete
    Backup->>Notification: Send notification (if enabled)
    Notification-->>Backup: Sent
    Backup-->>Ansible: Backup complete
    Ansible-->>User: Backup saved to /var/nexus/backup/
```

## Data Flow

```mermaid
graph LR
    A[group_vars/nexus.yml] --> B[Role defaults]
    B --> C[Task variables]
    C --> D[Nexus REST API]
    D --> E[Nexus Server]

    style A fill:#fff3e0
    style D fill:#e8f5e9
    style E fill:#e1f5fe
```

## API Flow

```mermaid
graph TD
    A[Role] --> B[URI Module]
    B --> C[HTTP Request]
    C --> D[Nexus REST API]
    D --> E[Response]
    E --> F{Status?}
    F -->|200/201| G[Success]
    F -->|400| H[Already Exists]
    F -->|401| I[Auth Error]
    F -->|500| J[Server Error]

    style G fill:#c8e6c9
    style H fill:#fff9c4
    style I fill:#ffcdd2
    style J fill:#ffcdd2
```

## Security Model

```mermaid
graph TD
    A[Admin User] --> B[Nexus API]
    B --> C{Authentication}
    C -->|Basic Auth| D[Internal DB]
    C -->|LDAP| E[LDAP Server]
    C -->|Token| F[API Token]
    D --> G{Authorization}
    E --> G
    F --> G
    G -->|Roles| H[Access Control]
    H --> I[Repository Access]

    style A fill:#fce4ec
    style H fill:#e8f5e9
```

## Storage Architecture

```mermaid
graph TD
    A[Repository] --> B{Storage Type}
    B -->|file| C[Local Filesystem]
    B -->|s3| D{S3 Provider}
    D -->|AWS| E[Amazon S3]
    D -->|MinIO| F[MinIO Server]
    D -->|Other| G[S3-Compatible]
    C --> H[Blob Store]
    E --> H
    F --> H
    G --> H
    H --> I[Nexus Data]

    style C fill:#e8f5e9
    style E fill:#fff3e0
    style F fill:#e0f2f1
```
