# Troubleshooting

## Common Issues

### Nexus Won't Start

**Symptoms:** Service fails to start, port not responding

**Checks:**
```bash
# Check service status
systemctl status nexus

# Check logs
journalctl -u nexus -f

# Check Java
java -version

# Check disk space
df -h /var/nexus/data
```

**Solutions:**
- Verify Java is installed: `java -version`
- Check disk space: `df -h`
- Check port conflict: `ss -tlnp | grep 8081`
- Check permissions: `ls -la /var/nexus/data`

---

### API Not Responding

**Symptoms:** Health check fails, cannot access UI

**Checks:**
```bash
# Test API
curl -v http://localhost:8081/service/rest/v1/status

# Check service
systemctl status nexus

# Check logs
tail -f /var/nexus/data/log/nexus.log
```

**Solutions:**
- Wait for startup (can take 2-5 minutes)
- Check firewall: `firewall-cmd --list-ports`
- Check nexus_listen_address binding

---

### Backup Fails

**Symptoms:** Backup script errors, no backup created

**Checks:**
```bash
# Check backup directory
ls -la /var/nexus/backup/

# Run backup manually
/usr/local/bin/nexus-backup.sh

# Check disk space
df -h /var/nexus/backup
```

**Solutions:**
- Ensure backup directory exists and is writable
- Check disk space
- Verify nexus user permissions

---

### Restore Fails

**Symptoms:** Checksum mismatch, service won't start after restore

**Checks:**
```bash
# Verify backup integrity
sha256sum -c /var/nexus/backup/nexus-backup-xxx.tar.gz.sha256

# Check service
systemctl status nexus

# Check logs
journalctl -u nexus -f
```

**Solutions:**
- Use a different backup file
- Check Nexus version compatibility
- Verify backup file is not corrupted

---

### Upgrade Fails

**Symptoms:** Version mismatch, service won't start

**Checks:**
```bash
# Check current version
/opt/sonatype/current/bin/nexus --version

# Check target version
grep nexus_version group_vars/all/nexus.yml

# Check logs
journalctl -u nexus -f
```

**Solutions:**
- Restore from pre-upgrade backup
- Verify download URL is accessible
- Check disk space

---

### LDAP Authentication Fails

**Symptoms:** Users can't login, LDAP errors in logs

**Checks:**
```bash
# Test LDAP connection
ldapsearch -H ldap://ldap.example.com -D "cn=admin,dc=example,dc=com" -W -b "dc=example,dc=com"

# Check Nexus logs
grep -i ldap /var/nexus/data/log/nexus.log
```

**Solutions:**
- Verify LDAP host/port
- Verify bind DN and password
- Check base DN
- Verify user search filter

---

### Docker Container Issues

**Symptoms:** Container won't start, health check fails

**Checks:**
```bash
# Check container status
docker ps -a | grep nexus

# Check container logs
docker logs nexus

# Check container health
docker inspect nexus | grep -A5 Health
```

**Solutions:**
- Verify Docker is running
- Check volume permissions
- Verify network connectivity
- Check resource limits

---

### Disk Space Issues

**Symptoms:** Writes fail, cleanup errors

**Checks:**
```bash
# Check disk usage
df -h

# Check large files
du -sh /var/nexus/data/*

# Check blob stores
du -sh /var/nexus/data/blobs/*
```

**Solutions:**
- Run cleanup policies
- Expand storage
- Move blob stores to larger disk
- Configure soft quotas

---

## Debug Mode

Run with verbose output:

```bash
ansible-playbook -i inventories/production/inventory.yml playbooks/nexus_deploy.yml -vvv
```

## Getting Help

1. Check [FAQ](faq.md)
2. Search GitHub Issues
3. Create a new issue with:
   - Ansible version
   - Nexus version
   - OS version
   - Error logs
   - Steps to reproduce
