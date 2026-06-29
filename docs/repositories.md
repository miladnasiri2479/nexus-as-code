# Repository Examples

## Supported Formats

| Format | Hosted | Proxy | Group |
|---|---|---|---|
| maven2 | ✅ | ✅ | ✅ |
| docker | ✅ | ✅ | ✅ |
| npm | ✅ | ✅ | ✅ |
| pypi | ✅ | ✅ | ✅ |
| helm | ✅ | ✅ | ✅ |
| nuget | ✅ | ✅ | ✅ |
| raw | ✅ | ✅ | ❌ |
| go | ✅ | ✅ | ✅ |
| yum | ✅ | ✅ | ❌ |
| apt | ✅ | ✅ | ❌ |
| conan | ✅ | ✅ | ❌ |
| rubygems | ✅ | ✅ | ❌ |
| composer | ✅ | ✅ | ❌ |
| r | ✅ | ✅ | ❌ |
| gitlfs | ✅ | ❌ | ❌ |
| cocoapods | ❌ | ✅ | ❌ |

## Maven

```yaml
nexus_repos:
  # ── Hosted: Releases ──
  - name: maven-releases
    format: maven2
    type: hosted
    write_policy: allow_once
    version_policy: release
    layout_policy: strict
    strict_content_validation: true
    blob_store_name: default
    cleanup_policy: ""

  # ── Hosted: Snapshots ──
  - name: maven-snapshots
    format: maven2
    type: hosted
    write_policy: allow
    version_policy: snapshot
    layout_policy: permissive
    strict_content_validation: false
    blob_store_name: default
    cleanup_policy: maven-snapshot-cleanup

  # ── Proxy: Maven Central ──
  - name: maven-central
    format: maven2
    type: proxy
    remote_url: https://repo1.maven.org/maven2
    version_policy: release
    layout_policy: permissive
    strict_content_validation: true
    cache_max_age_in_minutes: 1440
    blob_store_name: default

  # ── Proxy: Google Maven ──
  - name: google-maven
    format: maven2
    type: proxy
    remote_url: https://maven.google.com
    version_policy: release
    layout_policy: permissive
    blob_store_name: default

  # ── Group: Public ──
nexus_repo_groups:
  - name: maven-public
    format: maven2
    member_repos:
      - maven-releases
      - maven-snapshots
      - maven-central
```

## Docker

```yaml
nexus_repos:
  # ── Hosted: Private images ──
  - name: docker-hosted
    format: docker
    type: hosted
    write_policy: allow
    v1_enabled: false
    force_basic_auth: false
    http_port: 0
    https_port: 0
    compress: true
    strict_content_validation: false
    blob_store_name: default

  # ── Proxy: Docker Hub ──
  - name: docker-hub
    format: docker
    type: proxy
    remote_url: https://registry-1.docker.io
    index_type: dockerhub
    v1_enabled: false
    compress: true
    cache_max_age_in_minutes: 1440
    blob_store_name: default

  # ── Proxy: GitHub Container Registry ──
  - name: ghcr-proxy
    format: docker
    type: proxy
    remote_url: https://ghcr.io
    index_type: registry
    index_url: https://ghcr.io
    compress: true
    blob_store_name: default

  # ── Proxy: Quay.io ──
  - name: quay-proxy
    format: docker
    type: proxy
    remote_url: https://quay.io
    index_type: registry
    index_url: https://quay.io/api/v1
    blob_store_name: default

  # ── Proxy: Kubernetes Registry ──
  - name: k8s-registry
    format: docker
    type: proxy
    remote_url: https://registry.k8s.io
    index_type: registry
    blob_store_name: default

  # ── Proxy: Red Hat Registry ──
  - name: redhat-registry
    format: docker
    type: proxy
    remote_url: https://registry.redhat.io
    index_type: registry
    blob_store_name: default

  # ── Proxy: Elastic ──
  - name: elastic-registry
    format: docker
    type: proxy
    remote_url: https://docker.elastic.co
    index_type: registry
    blob_store_name: default

  # ── Proxy: Harbor ──
  - name: harbor-proxy
    format: docker
    type: proxy
    remote_url: https://harbor.internal
    index_type: registry
    index_url: https://harbor.internal
    force_basic_auth: true
    blob_store_name: default

nexus_repo_groups:
  - name: docker-group
    format: docker
    member_repos:
      - docker-hosted
      - docker-hub
```

## NPM

```yaml
nexus_repos:
  - name: npm-hosted
    format: npm
    type: hosted
    write_policy: allow
    blob_store_name: default

  - name: npm-proxy
    format: npm
    type: proxy
    remote_url: https://registry.npmjs.org
    cache_max_age_in_minutes: 1440
    blob_store_name: default

nexus_repo_groups:
  - name: npm-group
    format: npm
    member_repos:
      - npm-hosted
      - npm-proxy
```

## PyPI

```yaml
nexus_repos:
  - name: pypi-hosted
    format: pypi
    type: hosted
    write_policy: allow
    blob_store_name: default

  - name: pypi-proxy
    format: pypi
    type: proxy
    remote_url: https://pypi.org/simple
    cache_max_age_in_minutes: 1440
    blob_store_name: default

nexus_repo_groups:
  - name: pypi-group
    format: pypi
    member_repos:
      - pypi-hosted
      - pypi-proxy
```

## Helm

```yaml
nexus_repos:
  - name: helm-hosted
    format: helm
    type: hosted
    write_policy: allow_once
    allow_redeploy: false
    blob_store_name: default

  - name: helm-stable
    format: helm
    type: proxy
    remote_url: https://charts.helm.sh/stable
    cache_max_age_in_minutes: 1440
    blob_store_name: default

  - name: helm-bitnami
    format: helm
    type: proxy
    remote_url: https://charts.bitnami.com/bitnami
    cache_max_age_in_minutes: 1440
    blob_store_name: default

nexus_repo_groups:
  - name: helm-group
    format: helm
    member_repos:
      - helm-hosted
      - helm-stable
      - helm-bitnami
```

## Go

```yaml
nexus_repos:
  - name: go-hosted
    format: go
    type: hosted
    write_policy: allow
    blob_store_name: default

  - name: go-proxy
    format: go
    type: proxy
    remote_url: https://proxy.golang.org
    cache_max_age_in_minutes: 1440
    blob_store_name: default

nexus_repo_groups:
  - name: go-group
    format: go
    member_repos:
      - go-hosted
      - go-proxy
```

## NuGet

```yaml
nexus_repos:
  - name: nuget-hosted
    format: nuget
    type: hosted
    write_policy: allow
    blob_store_name: default

  - name: nuget-proxy
    format: nuget
    type: proxy
    remote_url: https://api.nuget.org/v3/index.json
    cache_max_age_in_minutes: 1440
    blob_store_name: default

nexus_repo_groups:
  - name: nuget-group
    format: nuget
    member_repos:
      - nuget-hosted
      - nuget-proxy
```

## Raw

```yaml
nexus_repos:
  - name: raw-hosted
    format: raw
    type: hosted
    write_policy: allow_once
    strict_content_validation: false
    blob_store_name: default

  - name: raw-proxy
    format: raw
    type: proxy
    remote_url: https://releases.example.com
    cache_max_age_in_minutes: 1440
    blob_store_name: default
```

## APT

```yaml
nexus_repos:
  - name: ubuntu-proxy
    format: apt
    type: proxy
    remote_url: https://archive.ubuntu.com/ubuntu
    distribution: focal
    blob_store_name: default

  - name: apt-hosted
    format: apt
    type: hosted
    write_policy: allow
    distribution: focal
    blob_store_name: default
```

## YUM

```yaml
nexus_repos:
  - name: centos-proxy
    format: yum
    type: proxy
    remote_url: https://mirror.centos.org/centos/8/BaseOS/x86_64/os/
    deploy_policy: permissive
    repodata_depth: 1
    blob_store_name: default

  - name: yum-hosted
    format: yum
    type: hosted
    write_policy: allow
    deploy_policy: permissive
    blob_store_name: default
```
