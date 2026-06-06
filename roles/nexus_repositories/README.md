# Nexus Repositories Role

This role automates the dynamic provisioning, updating, and **deletion** of Nexus repositories via the REST API based on a predefined catalog.

## Features
- **Catalog Based**: Uses `vars/catalog.yml` as the internal source of truth for the exact API payload required for each repo type (Docker, Maven, NPM, PyPI, Helm).
- **Dynamic State Management**: Iterates over your `repositories` dictionary:
  - If `enabled: true` and missing -> **POST** (Create)
  - If `enabled: true` and exists -> **PUT** (Update)
  - If `enabled: false` and exists -> **DELETE** (Remove)
- **Dynamic Blobstore Binding**: Easily map a repository to a specific blobstore. If not mapped, it gracefully falls back to the default specified in the catalog.
- **Strictly Idempotent**: Fetches the list of existing repositories first to determine the exact action required, preventing redundant API mutative calls.
- **Storage Agnostic**: This role doesn't care if the blobstore is File, S3, or MinIO. It simply binds to the blobstore name, relying on the `nexus_blobstores` role to handle the storage abstraction.

## Variables

Define your repositories in `group_vars/all.yml`.

```yaml
repositories:
  docker_hub:
    enabled: true
    blobstore: "docker" # Binds to the blobstore named "docker"

  maven_central:
    enabled: true
    blobstore: "maven"

  npm_registry:
    enabled: false # If it currently exists in Nexus, it WILL BE DELETED.

  helm_charts:
    enabled: true
```
