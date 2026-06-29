# MinIO Examples

## Standalone MinIO

```yaml
nexus_storage_minio:
  enabled: true
  version: "RELEASE.2024-01-16T16-07-38Z"
  port: 9000
  console_port: 9001
  access_key: "{{ vault_minio_access_key }}"
  secret_key: "{{ vault_minio_secret_key }}"
  data_dir: /data/minio
  tls_enabled: false

nexus_buckets:
  - name: nexus-blobs
    versioning: false

  - name: nexus-backups
    versioning: true
```

## MinIO with TLS

```yaml
nexus_storage_minio:
  enabled: true
  port: 9000
  console_port: 9001
  access_key: "{{ vault_minio_access_key }}"
  secret_key: "{{ vault_minio_secret_key }}"
  data_dir: /data/minio
  tls_enabled: true
  cert_dir: /etc/minio/certs

# Place certificates:
# /etc/minio/certs/private.key
# /etc/minio/certs/public.crt
```

## MinIO Erasure Coding (Multi-Disk)

```yaml
nexus_storage_minio:
  enabled: true
  port: 9000
  access_key: "{{ vault_minio_access_key }}"
  secret_key: "{{ vault_minio_secret_key }}"
  volumes: "/data1 /data2 /data3 /data4"
```

## MinIO with Nexus S3

```yaml
nexus_storage_type: s3

nexus_storage_s3:
  enabled: true
  region: us-east-1
  bucket_prefix: nexus
  access_key_id: "{{ vault_minio_access_key }}"
  secret_access_key: "{{ vault_minio_secret_key }}"
  endpoint: "http://minio.internal:9000"
  path_style_access: true

nexus_blobstores:
  - name: default
    type: s3
    s3:
      region: us-east-1
      bucket: nexus-default
      access_key_id: "{{ vault_minio_access_key }}"
      secret_access_key: "{{ vault_minio_secret_key }}"
      endpoint: "http://minio.internal:9000"
      path_style_access: true
```

## MinIO Bucket Validation

```bash
# Validate MinIO buckets
ansible-playbook -i inventories/production/inventory.yml playbooks/nexus_validate.yml --tags storage,buckets
```
