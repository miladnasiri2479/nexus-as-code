# nexus_security

Configure Nexus Repository Manager security settings.

## Description

This role configures:
- Anonymous access
- Security realms
- SSL/TLS settings
- Admin password validation

## Requirements

- Nexus Repository Manager must be installed and running
- Admin credentials must be set

## Role Variables

### Required

| Variable | Description | Default |
|---|---|---|
| `nexus_admin_password` | Admin password | `""` |

### Optional

| Variable | Description | Default |
|---|---|---|
| `nexus_anonymous_access_enabled` | Enable anonymous access | `false` |
| `nexus_anonymous_user` | Anonymous user ID | `anonymous` |
| `nexus_anonymous_realm` | Anonymous realm | `nx-anonymous` |
| `nexus_realms` | Active security realms | `[NexusAuthenticatingRealm, NexusAuthoringRealm]` |
| `nexus_ssl_enabled` | Enable SSL | `false` |
| `nexus_ssl_keystore` | Path to keystore | `""` |
| `nexus_security_force_ssl` | Force SSL | `false` |
| `nexus_security_run_once` | Run once in multi-host | `false` |
| `nexus_security_delegate_to` | Delegate to host | `""` |
| `nexus_api_retries` | API retry count | `3` |
| `nexus_api_retry_delay` | Retry delay (seconds) | `5` |

## Dependencies

None

## Example Playbook

```yaml
- hosts: nexus
  roles:
    - role: nexus_security
      vars:
        nexus_admin_password: "{{ vault_nexus_admin_password }}"
        nexus_anonymous_access_enabled: false
        nexus_realms:
          - NexusAuthenticatingRealm
          - NexusAuthoringRealm
          - LdapRealm
```

## Tags

| Tag | Description |
|---|---|
| `nexus` | All Nexus tasks |
| `security` | All security tasks |
| `validate` | Validation tasks |
| `anonymous` | Anonymous access tasks |
| `realms` | Realm configuration tasks |
| `ssl` | SSL/TLS tasks |
| `config` | Configuration tasks |
| `summary` | Summary output |

## License

Apache-2.0

## Author

nexus-as-code
