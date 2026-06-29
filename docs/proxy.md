# Proxy Examples

## HTTP Proxy

```yaml
nexus_proxy_enabled: true

nexus_http_proxy_host: proxy.example.com
nexus_http_proxy_port: 3128
nexus_http_proxy_username: proxyuser
nexus_http_proxy_password: "{{ vault_proxy_password }}"

nexus_no_proxy_hosts: "localhost,127.0.0.1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,.internal.example.com"
```

## HTTPS Proxy

```yaml
nexus_proxy_enabled: true

nexus_https_proxy_host: proxy.example.com
nexus_https_proxy_port: 8443
nexus_https_proxy_username: proxyuser
nexus_https_proxy_password: "{{ vault_proxy_password }}"

nexus_no_proxy_hosts: "localhost,127.0.0.1,.internal.example.com"
```

## Proxy with No Auth

```yaml
nexus_proxy_enabled: true

nexus_http_proxy_host: proxy.example.com
nexus_http_proxy_port: 8080
nexus_http_proxy_username: ""
nexus_http_proxy_password: ""

nexus_no_proxy_hosts: "localhost,127.0.0.1,10.0.0.0/8"
```

## Corporate Proxy

```yaml
nexus_proxy_enabled: true

nexus_http_proxy_host: internet-proxy.corp.example.com
nexus_http_proxy_port: 8080
nexus_http_proxy_username: "{{ vault_proxy_user }}"
nexus_http_proxy_password: "{{ vault_proxy_pass }}"

nexus_https_proxy_host: internet-proxy.corp.example.com
nexus_https_proxy_port: 8443
nexus_https_proxy_username: "{{ vault_proxy_user }}"
nexus_https_proxy_password: "{{ vault_proxy_pass }}"

nexus_no_proxy_hosts: >-
  localhost,
  127.0.0.1,
  10.0.0.0/8,
  172.16.0.0/12,
  192.168.0.0/16,
  .corp.example.com,
  .internal.example.com
```

## Docker Behind Proxy

```yaml
# When Nexus runs in Docker behind a proxy
nexus_docker_env:
  HTTP_PROXY: "http://proxy.example.com:8080"
  HTTPS_PROXY: "http://proxy.example.com:8443"
  NO_PROXY: "localhost,127.0.0.1,.internal.example.com"
```
