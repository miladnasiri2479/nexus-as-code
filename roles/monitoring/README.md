# Nexus Monitoring Role

Provides an extremely lightweight, non-invasive observability configuration for Sonatype Nexus. It does **not** install a heavy Prometheus or Grafana stack. Instead, it securely exposes the necessary endpoints so your existing enterprise monitoring tools can scrape Nexus.

## Execution Rule
This role executes **ONLY IF**:
```yaml
features:
  monitoring:
    enabled: true
```

## Features
- **Basic Health Checks**: Validates the core system APIs without generating heavy loads.
- **Least-Privilege Setup**: Creates a dedicated `nexus-monitor` role equipped strictly with the `nx-metrics-all` and `nx-healthcheck-read` privileges.
- **Dedicated Scrape User**: Creates an API-only user (default: `monitor`) bound to the role. 
- **Non-Invasive**: No additional containers, sidecars, or Java agents are injected. It strictly leverages the native Nexus 3 `/service/rest/v1/status/prometheus` endpoint.

## Variables
Configure in your `group_vars/all.yml`:

```yaml
features:
  monitoring:
    enabled: true
    metrics_enabled: true
    user: "nexus_scraper"
    password: "SecureScraperPassword!"
```

## Scraping the Endpoint
Once this role executes, you can configure your external Prometheus server or Datadog agent to scrape the target using Basic Auth:

**URL:** `https://<nexus_domain>/service/rest/v1/status/prometheus`
**Username:** (from `features.monitoring.user`)
**Password:** (from `features.monitoring.password`)
