# Nexus Docker Role

This role deploys Sonatype Nexus as a Docker container. It is designed to be fully idempotent, production-ready, and adheres to Ansible best practices by exclusively using native Ansible modules (no shell commands).

## Features
- **Docker Setup**: Automatically installs Docker and its Python bindings based on OS (`Debian` or `RedHat`).
- **Networking**: Creates an isolated, dedicated Docker network.
- **Persistent Storage**: Configures the host directory with correct permissions (`UID 200` for Nexus).
- **Resilience**: Configures a health check and an `unless-stopped` restart policy.
- **Safety**: Actively polls the Nexus API endpoint to verify readiness before handing execution back to the playbook.

## Variables
Available variables in `nexus` dictionary (usually set in `group_vars/all.yml`):
- `nexus.version`: The Nexus Docker image tag (e.g., `3.68.0`).
- `nexus.data_dir`: Absolute path on the host for persistent data (e.g., `/opt/nexus-data`).
- `nexus.http_port`: Port exposed on the host for web access (e.g., `8081`).
- `nexus.network_name`: Name of the Docker network.

## Dependencies
This role uses the `community.docker` Ansible collection. Make sure it is installed (e.g., via `requirements.yml`):
```yaml
collections:
  - name: community.docker
```
