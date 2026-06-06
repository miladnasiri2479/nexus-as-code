# Traefik Reverse Proxy Role

This role deploys Traefik as a reverse proxy in front of Sonatype Nexus. It handles automatic HTTP to HTTPS redirection, optional Let's Encrypt automated certificates, and routes traffic securely into the internal Docker network.

## Features
- **Docker Native**: Runs seamlessly alongside your Nexus container.
- **Let's Encrypt**: Native support for automatic SSL/TLS certificate generation via HTTP-01 challenge.
- **Auto Redirect**: Forcefully redirects all port 80 traffic to 443.
- **File Provider**: Uses Traefik's dynamic file provider to route traffic to Nexus. This means we don't have to alter the Nexus container's labels (clean separation of concerns).
- **Dashboard**: Optional dashboard can be enabled for debugging.

## Variables

Set these in your `group_vars/all.yml`:

```yaml
traefik:
  enabled: true                 # Set to false to skip this role
  version: "v2.10"
  domain: "nexus.mycompany.com" # The domain routing to Nexus
  letsencrypt: true             # Enable automatic SSL
  email: "admin@mycompany.com"  # Required for Let's Encrypt recovery
  dashboard_enabled: false      # Enable Traefik's internal dashboard API
```

## How It Works
1. The role creates a directory at `/opt/traefik`.
2. It templates a static `traefik.yml` (entrypoints, cert resolvers).
3. It templates a dynamic `dynamic/nexus.yml` (routers and services mapping to the internal Nexus container).
4. An empty `acme.json` with strict `0600` permissions is created to safely store Let's Encrypt certs.
5. Traefik is launched on the host's `80` and `443` ports, connected to the `nexus_network`.
