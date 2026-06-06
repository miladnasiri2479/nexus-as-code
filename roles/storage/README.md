# Storage Validation Role

This role provides an **OPTIONAL** validation layer for Nexus storage backends before Nexus is configured to use them. It ensures that if an external object storage is requested, the credentials and connectivity are fully verified, preventing complex failures later in the pipeline.

## Features
- **File Storage Default**: If `storage.type: file` is set (the default), the role safely ignores validation.
- **Fail-Fast**: Immediately stops execution if required credentials are missing for external storage.
- **AWS S3 & MinIO Support**: Validates connectivity, credential authenticity, and bucket existence.
- **Idempotent & Safe**: Purely read-only checks. It **DOES NOT** provision buckets.

## Variables
Define your storage configuration in `group_vars/all.yml`:

### Local File (Default)
```yaml
storage:
  type: "file"
```

### AWS S3
```yaml
storage:
  type: "s3"
  bucket: "my-nexus-bucket"
  access_key: "AKIA..."
  secret_key: "SECRET..."
  region: "us-east-1"
```

### MinIO
```yaml
storage:
  type: "minio"
  bucket: "nexus-artifacts"
  endpoint: "https://minio.internal.company.local"
  access_key: "MINIO_USER"
  secret_key: "MINIO_PASS"
```

## Dependencies
If `storage.type` is set to `s3` or `minio`, this role requires the `amazon.aws` collection and the `boto3` Python package installed on the executing machine.
```bash
ansible-galaxy collection install amazon.aws
pip install boto3 botocore
```
