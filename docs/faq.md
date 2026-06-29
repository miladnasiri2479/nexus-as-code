# FAQ

## General

### What is Nexus as Code?

An Ansible project for deploying and managing Sonatype Nexus Repository Manager. It provides 30+ roles for complete lifecycle management.

### What Nexus versions are supported?

Nexus Repository Manager 3.x (OSS and Pro editions).

### What operating systems are supported?

- RHEL 8/9
- Ubuntu 20.04/22.04/24.04
- Debian 11/12

### Do I need to install Java?

No. The `java` role installs OpenJDK 17 automatically.

---

## Installation

### How do I install?

```bash
git clone https://github.com/nexus-as-code/nexus-as-code.git
cd nexus-as-code
vim inventories/production/group_vars/nexus.yml
ansible-playbook -i inventories/production/inventory.yml playbooks/nexus_deploy.yml
```

### Can I install behind a proxy?

Yes. Set `nexus_download_proxy` variables in your inventory.

### Can I use a local mirror?

Yes. Set `nexus_download_url` to your local mirror URL.

---

## Configuration

### Where do I configure Nexus?

Edit `inventories/<env>/group_vars/nexus.yml`. This is the only file you need to edit.

### How do I add a repository?

Add an entry to `nexus_repos`:

```yaml
nexus_repos:
  - name: my-repo
    format: maven2
    type: hosted
    write_policy: allow_once
```

### How do I enable Docker support?

```yaml
nexus_repos:
  - name: docker-hosted
    format: docker
    type: hosted
    write_policy: allow
    http_port: 5000
```

### How do I configure LDAP?

```yaml
nexus_ldap_enabled: true
nexus_ldap:
  host: ldap.example.com
  port: 389
  base_dn: "dc=example,dc=com"
  bind_dn: "cn=nexus,ou=service,dc=example,dc=com"
  bind_password: "{{ vault_ldap_password }}"
```

---

## Storage

### Can I use S3?

Yes. Set `nexus_storage_type: s3` and configure `nexus_storage_s3`.

### Can I use MinIO?

Yes. Enable MinIO with `nexus_storage_minio.enabled: true`.

### How do I migrate to S3?

1. Create S3 bucket
2. Update inventory to S3 storage
3. Run `ansible-playbook nexus_deploy.yml`
4. Use Nexus migration tool for existing data

---

## Operations

### How do I backup?

```bash
ansible-playbook -i inventories/production/inventory.yml playbooks/nexus_backup.yml
```

### How do I restore?

```bash
ansible-playbook -i inventories/production/inventory.yml playbooks/nexus_restore.yml \
  -e "nexus_restore_source=/path/to/backup.tar.gz"
```

### How do I upgrade?

```bash
ansible-playbook -i inventories/production/inventory.yml playbooks/nexus_upgrade.yml \
  -e "nexus_version=3.73.0"
```

### How do I check health?

```bash
ansible-playbook -i inventories/production/inventory.yml playbooks/nexus_validate.yml
```

---

## Troubleshooting

### Nexus won't start

1. Check Java: `java -version`
2. Check disk space: `df -h`
3. Check logs: `journalctl -u nexus -f`
4. Check port: `ss -tlnp | grep 8081`

### API not responding

1. Wait 2-5 minutes for startup
2. Check firewall: `firewall-cmd --list-ports`
3. Check logs: `tail -f /var/nexus/data/log/nexus.log`

### Backup fails

1. Check disk space: `df -h /var/nexus/backup`
2. Check permissions: `ls -la /var/nexus/backup`
3. Run manually: `/usr/local/bin/nexus-backup.sh`

---

## Security

### How do I change the admin password?

Update `nexus_admin_password` in your inventory and run the playbook.

### How do I disable anonymous access?

```yaml
nexus_anonymous_access_enabled: false
```

### How do I add users?

```yaml
nexus_users:
  - userId: developer
    password: "{{ vault_dev_password }}"
    roles:
      - nx-developer
```

---

## Development

### How do I add a new role?

See the [Developer Guide](developer.md).

### How do I run tests?

```bash
cd roles/my_role
molecule test
```

### How do I contribute?

See the [Contribution Guide](contributing.md).
