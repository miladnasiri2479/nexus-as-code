# Nexus Bootstrap Role

This role is responsible for the initial configuration of Nexus immediately after it boots up. It exclusively uses the `ansible.builtin.uri` module to interact with the Nexus REST API.

## Features
- **Idempotent Password Management**: Checks if the target `admin` password is already set. If not, it reads the initial auto-generated password from the data directory and changes it.
- **Security Configuration**: Disables (or configures) anonymous access based on your requirements.
- **Docker Ready**: Automatically enables the `DockerToken` realm which is required for Docker registry authentication.
- **No Shell Scripts**: Operates 100% over HTTP REST API to guarantee idempotency and avoid complex groovy scripts.

## Variables
Available variables in `nexus` dictionary:
- `nexus.hostname`: The domain name of the Nexus instance.
- `nexus.http_port`: Internal HTTP port for API communication (default: `8081`).
- `nexus.data_dir`: The host directory where Nexus stores its data (used to read `admin.password`).
- `nexus.admin_password`: The desired secure password for the `admin` user.
- `nexus.anonymous_access`: Boolean to enable or disable anonymous read access (default: `false`).

## Note on Base URL
Nexus 3 automatically infers the Base URL from the incoming request headers (e.g., `X-Forwarded-Proto`, `X-Forwarded-Host` set by Traefik). Configuring it strictly via the API is usually unnecessary when properly proxied, but can be managed via UI Capabilities if strict override is required.
