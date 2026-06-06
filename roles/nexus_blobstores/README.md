# Dynamic Nexus Blobstores Role

This role dynamically manages Sonatype Nexus blobstores via the REST API. It inherits its configuration context from the global `storage.type` variable.

## Features
- **Global Storage Context**: Determines the blobstore type based on `storage.type` (`file`, `s3`, or `minio`).
- **Dictionary Driven**: Iterates over a dictionary of `blobstores`, automatically skipping those where `enabled: false`.
- **S3 Prefix Mapping**: When using S3 or MinIO, it maps all blobstores to a single bucket (`storage.bucket`) and uses the blobstore's name as the bucket `prefix`. This is best practice for cost and organization.
- **MinIO Ready**: Automatically sets `forcePathStyle: true` if `storage.type: minio`.
- **Idempotent**: Fetches the list of existing blobstores first. Missing ones are `POST`ed. Existing ones are `PUT` updated.

## Variables

Define your blobstores and storage context in `group_vars/all.yml`:

```yaml
# Global context (validated by the `storage` role)
storage:
  type: "minio" # or 'file', or 's3'
  bucket: "my-nexus-artifacts"
  endpoint: "https://minio.internal.local"
  access_key: "admin"
  secret_key: "Password123"

# Dictionary of blobstores to provision
blobstores:
  docker:
    enabled: true
  maven:
    enabled: true
  npm:
    enabled: false # Will be skipped safely
```
