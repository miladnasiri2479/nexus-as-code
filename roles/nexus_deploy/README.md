# Nexus Deploy Role

Deploys Sonatype Nexus inside a Docker container. Ensures all underlying infrastructure (Docker daemon, networks, storage volumes) is correctly configured before booting the service.

## Features
- **Docker Validation**: Installs Docker and the `python3-docker` SDK required by Ansible.
- **Persistent Storage**: Ensures the data directory exists and is owned by UID `200` (required by the `sonatype/nexus3` image).
- **Idempotency**: Utilizes `community.docker.docker_container`. Will not recreate the container if the configuration matches the desired state.
- **Readiness Check**: Implements a native Docker health check and blocks Ansible execution via `ansible.builtin.uri` polling until the Nexus API returns HTTP 200.

## Variables
Available variables in `nexus` dictionary (usually set in `group_vars/all.yml`):
- `nexus.version`: The Nexus Docker image tag (e.g., `3.68.0`).
- `nexus.data_dir`: Absolute path on the host for persistent data (default: `/opt/nexus-data`).
- `nexus.http_port`: Port exposed on the host for web access (default: `8081`).
- `nexus.network_name`: Name of the Docker network (default: `nexus-net`).
- `nexus.container_name`: Name of the Docker container (default: `nexus`).

## Dependencies
Requires the `community.docker` Ansible collection.
