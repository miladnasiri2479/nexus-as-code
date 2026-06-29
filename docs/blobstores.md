# Blob Store Examples

## Local Filesystem

```yaml
nexus_blobstores:
  - name: default
    type: file
    soft_quota: ""
    file:
      path: /data/nexus

  - name: maven-storage
    type: file
    soft_quota: 1TB
    file:
      path: /data/nexus/maven

  - name: docker-storage
    type: file
    soft_quota: 500GB
    file:
      path: /data/nexus/docker
```

## S3 (AWS)

```yaml
nexus_blobstores:
  - name: s3-default
    type: s3
    soft_quota: 1TB
    s3:
      region: us-east-1
      bucket: my-nexus-blobs
      access_key_id: "{{ vault_s3_access_key }}"
      secret_access_key: "{{ vault_s3_secret_key }}"
      path_style_access: false

  - name: s3-docker
    type: s3
    soft_quota: 500GB
    s3:
      region: us-west-2
      bucket: my-nexus-docker
      access_key_id: "{{ vault_s3_access_key }}"
      secret_access_key: "{{ vault_s3_secret_key }}"
```

## S3 (MinIO)

```yaml
nexus_blobstores:
  - name: minio-storage
    type: s3
    soft_quota: 2TB
    s3:
      region: us-east-1
      bucket: nexus-blobs
      access_key_id: "{{ vault_minio_access_key }}"
      secret_access_key: "{{ vault_minio_secret_key }}"
      endpoint: "http://minio.internal:9000"
      path_style_access: true
```

## S3 (DigitalOcean Spaces)

```yaml
nexus_blobstores:
  - name: do-storage
    type: s3
    soft_quota: 1TB
    s3:
      region: nyc3
      bucket: my-nexus
      access_key_id: "{{ vault_do_access_key }}"
      secret_access_key: "{{ vault_do_secret_key }}"
      endpoint: "https://nyc3.digitaloceanspaces.com"
```

## Repository to Blobstore Mapping

```yaml
# Explicit mapping
nexus_repo_blobstore_map:
  maven-releases: maven-storage
  maven-snapshots: maven-storage
  docker-hosted: docker-storage
  docker-hub: docker-storage
  npm-hosted: default

# Format defaults
nexus_format_blobstore_defaults:
  maven2: maven-storage
  docker: docker-storage
  npm: default
  pypi: default
```
