# Nexus as Code

Production-grade Ansible project for deploying and managing Sonatype Nexus Repository Manager.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Ansible](https://img.shields.io/badge/Ansible-2.14+-green.svg)](https://www.ansible.com/)
[![Nexus](https://img.shields.io/badge/Nexus-3.x-orange.svg)](https://www.sonatype.com/products/repository-manager)

## Features

- **30+ Ansible roles** — fully modular, independent, reusable
- **Bare-metal + Docker** — choose your deployment method
- **All formats** — Maven, Docker, npm, PyPI, Helm, NuGet, Go, APT, YUM, Raw, Conan, RubyGems, Composer
- **S3 storage** — AWS S3, MinIO, DigitalOcean Spaces
- **Blob store management** — automatic creation and mapping
- **Repository groups** — transparent aggregation
- **Cleanup policies** — automatic artifact retention
- **Security** — users, roles, LDAP, anonymous access
- **Backup/Restore** — scheduled backups with S3 upload
- **Health checks** — API, disk, service, port verification
- **Zero hardcoded values** — everything configurable from one file

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/nexus-as-code/nexus-as-code.git
cd nexus-as-code

# 2. Edit inventory
vim inventories/production/group_vars/nexus.yml

# 3. Deploy
ansible-playbook -i inventories/production/inventory.yml playbooks/nexus_deploy.yml
```

## Requirements

| Requirement | Minimum |
|---|---|
| Ansible | 2.14+ |
| Python | 3.9+ |
| Target OS | RHEL 8/9, Ubuntu 20.04/22.04/24.04, Debian 11/12 |
| Java | OpenJDK 17 (installed automatically) |

## Installation

```bash
# Via git
git clone https://github.com/nexus-as-code/nexus-as-code.git

# Install dependencies
ansible-galaxy collection install community.docker
ansible-galaxy collection install community.general
ansible-galaxy collection install ansible.posix
```

## Playbooks

| Playbook | Purpose |
|---|---|
| `nexus_deploy.yml` | Full deployment (install + configure + validate) |
| `nexus_install.yml` | Install Nexus only |
| `nexus_configure.yml` | Configure repos, security, etc. |
| `nexus_backup.yml` | Run backup |
| `nexus_restore.yml` | Restore from backup |
| `nexus_upgrade.yml` | Upgrade to new version |
| `nexus_validate.yml` | Validate configuration |
| `nexus_destroy.yml` | Remove installation |

## Documentation

- [Architecture](docs/architecture.md)
- [Execution Flow](docs/execution-flow.md)
- [Variable Reference](docs/variables.md)
- [Repository Examples](docs/repositories.md)
- [Blob Store Examples](docs/blobstores.md)
- [S3 Examples](docs/s3.md)
- [MinIO Examples](docs/minio.md)
- [Proxy Examples](docs/proxy.md)
- [Backup Guide](docs/backup.md)
- [Restore Guide](docs/restore.md)
- [Upgrade Guide](docs/upgrade.md)
- [Developer Guide](docs/developer.md)
- [Contribution Guide](docs/contributing.md)
- [Troubleshooting](docs/troubleshooting.md)
- [FAQ](docs/faq.md)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    inventory.yml                        │
│                    group_vars/nexus.yml                 │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                    Playbooks                            │
│  deploy | install | configure | backup | restore | ...  │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                    Roles (30+)                          │
│  common → java → install → config → blobstores → ...   │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                    Nexus REST API                       │
│              http://nexus:8081/service/rest/v1/         │
└─────────────────────────────────────────────────────────┘
```

## Example Configuration

```yaml
# inventories/production/group_vars/nexus.yml

# Version
nexus_version: "3.72.0"
nexus_port: 8081

# Admin
nexus_admin_password: "{{ vault_nexus_admin_password }}"

# Storage
nexus_storage_type: file
nexus_storage_local:
  path: /data/nexus

# Repositories
nexus_repos:
  - name: maven-releases
    format: maven2
    type: hosted
    write_policy: allow_once
    version_policy: release

  - name: docker-hosted
    format: docker
    type: hosted
    write_policy: allow
    http_port: 5000
```

## License

Apache License 2.0

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
