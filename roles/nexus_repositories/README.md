# Nexus Repositories Role

This role automates the creation and configuration of Nexus repositories via the REST API based on a predefined catalog.

## Features
- **Catalog Based**: Uses `vars/catalog.yml` as the internal source of truth for the exact API payload required for each repo type (Docker, Maven, NPM, etc.).
- **Smart Filtering**: Iterates over your `repositories` dictionary and automatically **skips** any repository where `enabled: false` (or undefined).
- **Idempotent**: Fetches the list of existing repositories first. It uses `POST` to create missing repositories and `PUT` to update existing ones.
- **Dynamic Overrides**: You can override the default blobstore for a specific repository directly in your configuration.

## Variables

Define your repositories in `group_vars/all.yml`.

```yaml
repositories:
  docker_hub:
    enabled: true
    blobstore: "docker-s3-blob" # Optional override, otherwise uses 'default'

  maven_central:
    enabled: true

  npm_registry:
    enabled: false # Will be skipped
```

## Available Catalog Keys
Out of the box, the `vars/catalog.yml` supports:
- `docker_hub`
- `maven_central`
- `npm_registry`
- `pypi_org`
*(You can easily add more by copying payloads from the `docs/repository-catalog.yml` into `roles/repositories/vars/catalog.yml`).*
