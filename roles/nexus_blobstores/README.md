# Nexus Blobstores Role

This role dynamically manages Sonatype Nexus blobstores via the REST API. It handles both `file` and `s3` (including MinIO compatible) blobstores.

## Features
- **File and S3 Support**: Fully implements the complex API payload required for both types.
- **Idempotent Execution**: It first lists all blobstores. If a blobstore is missing, it sends a `POST` request. If it exists, it sends a `PUT` request to update settings.
- **MinIO Ready**: Automatically sets `forcePathStyle: true` if an S3 `endpoint` is provided (which is required for MinIO).
- **Secure**: All API calls containing credentials are masked via `no_log: true`.

## Variables

Define your blobstores in `group_vars/all.yml` under the `blobstores` list:

```yaml
nexus:
  admin_user: admin
  admin_password: YourPassword123!

blobstores:
  # Example File Blobstore
  - name: "my-local-blob"
    type: "file"
    path: "/nexus-data/custom-blob" # Optional, defaults to /nexus-data/blobs/<name>

  # Example S3 Blobstore (AWS)
  - name: "aws-s3-blob"
    type: "s3"
    bucket: "my-nexus-bucket"
    region: "us-east-1"
    access_key: "AKIA..."
    secret_key: "SECRET..."

  # Example MinIO (S3 Compatible)
  - name: "minio-blob"
    type: "s3"
    bucket: "nexus-artifacts"
    endpoint: "https://minio.mycompany.local"
    access_key: "MINIO_USER"
    secret_key: "MINIO_PASS"
```
