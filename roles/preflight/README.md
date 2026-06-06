# Preflight Role

This role acts as a strict validation gate before any deployment logic is executed. It ensures the target system meets all the necessary prerequisites for hosting Sonatype Nexus and Traefik.

## Features
- **Docker Validation**: Uses `service_facts` to strictly verify that `docker.service` exists and is `running`.
- **Port Checking**: Uses the `wait_for` module to ensure ports `8081` (Nexus), `80` (HTTP), and `443` (HTTPS) are free and not bound by other processes.
- **Disk Space Validation**: Analyzes Ansible's mount facts to ensure the partition hosting `nexus_data_path` has at least 10GB of free space.
- **Fail-Fast**: If any check fails, the playbook stops immediately with a human-readable error message.

## Variables
Available variables in `preflight` dictionary (can be overridden in `group_vars`):
- `preflight.nexus_port`: Port Nexus will bind to (default: `8081`).
- `preflight.traefik_http_port`: Port Traefik will bind to for HTTP (default: `80`).
- `preflight.traefik_https_port`: Port Traefik will bind to for HTTPS (default: `443`).
- `preflight.min_disk_space_gb`: Minimum required free disk space in Gigabytes (default: `10`).
- `preflight.nexus_data_path`: The path intended for Nexus data, used to determine which mount point to check for disk space (default: `/opt/nexus-data`).
