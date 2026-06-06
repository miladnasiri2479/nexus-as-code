# Nexus as Code

A production-grade, declarative, idempotent deployment and configuration engine for Sonatype Nexus. Built on Ansible, inspired by Kubespray's architecture.

## Architecture
This project separates **Infrastructure Deployment** from **Application Configuration**.
- **`install.yml`**: Uses Docker to deploy Nexus and Traefik (Edge proxy + Let's Encrypt).
- **`configure.yml`**: Communicates strictly via the Nexus REST API to handle passwords, security realms, blobstores, and repositories.

All configuration is driven by a single source of truth: `group_vars/all.yml`.

## Features
- **Idempotent by Design**: Run it 100 times, it only changes what needs changing.
- **Fail-Fast Validation**: Syntax and variable requirements are validated before deployment begins.
- **Dynamic Blobstores**: Fully automated local File or remote S3 / MinIO blobstore creation via REST API.
- **Repository Catalog**: Automatically deploys Docker Hub proxies, Maven Central, NPM, etc., based on simple boolean toggles.
- **TLS out-of-the-box**: Traefik automatically routes HTTP to HTTPS and provisions Let's Encrypt certificates.

## Quickstart

### 1. Copy the Sample Inventory
```bash
cp -rfp inventory/sample inventory/production
```

### 2. Configure your Environment
Edit `inventory/production/inventory.ini` and set your server IPs.
Edit `inventory/production/group_vars/all.yml` and set your desired state:
- Set `nexus.hostname` and `nexus.admin_password`.
- Toggle repositories (`docker_hub.enabled: true`).
- Configure blobstores (Local or S3).
- Enable `traefik.letsencrypt` if exposed to the internet.

### 3. Run the Playbook
To deploy and configure everything from scratch:
```bash
ansible-playbook -i inventory/production/inventory.ini site.yml
```

### Partial Runs (Tags)
Only run the API configuration (skip Docker checks):
```bash
ansible-playbook -i inventory/production/inventory.ini configure.yml
```
Update only Blobstores:
```bash
ansible-playbook -i inventory/production/inventory.ini configure.yml --tags "blobstores"
```
