# Nexus Bootstrap Role

This role configures Sonatype Nexus via its REST API immediately after the container boots up. It is strictly idempotent and safe to re-run.

## Features
1. **API Readiness**: Uses Ansible's `uri` module with retries to wait for the `/service/rest/v1/status` endpoint to become available.
2. **Password Setup**: Retrieves the initial generated admin password from the data directory and securely changes it via the API.
3. **Anonymous Access**: Idempotently enforces whether anonymous access is enabled or disabled.
4. **Security Realms**: Ensures required realms (like `DockerToken` and `NexusAuthenticatingRealm`) are enabled without disabling existing custom realms.
5. **Base URL**: Attempts to configure the Base URL using the Groovy Scripting API (Note: This requires `nexus.scripts.allowCreation=true` in modern Nexus versions; it fails gracefully if disabled).

## Strict Constraints Maintained
- **Ansible Native**: `ansible.builtin.uri` and `ansible.builtin.slurp` are the only modules used. No raw shell or curl commands.
- **Idempotent**: All endpoints are first queried with a `GET`. Mutative `PUT` requests only execute if state drift is detected.
- **Secure**: All tasks transmitting passwords implement `no_log: true` to protect CI/CD logs.

## Variables
Available variables (defined in `defaults/main.yml`):
- `nexus.admin_password`: Target secure password.
- `nexus.anonymous_access`: Boolean to enable/disable anonymous access.
- `nexus.base_url`: Target URL for the instance.
- `nexus.active_realms`: List of realms that must be present.
