# Developer Guide

## Project Structure

```
nexus-as-code/
├── roles/              # 30+ independent roles
├── playbooks/          # Orchestration playbooks
├── plugins/            # Custom modules/filters
├── inventories/        # Environment configurations
├── group_vars/         # Global defaults
├── files/              # Static files
├── tests/              # Molecule tests
└── docs/               # Documentation
```

## Adding a New Role

### 1. Create Directory Structure

```bash
mkdir -p roles/my_role/{tasks,handlers,defaults,meta,templates,files,vars}
```

### 2. Create `meta/main.yml`

```yaml
---
galaxy_info:
  role_name: my_role
  description: My new role
  author: nexus-as-code
  license: Apache-2.0
  min_ansible_version: "2.14"
  galaxy_tags: [nexus]
dependencies: []
```

### 3. Create `defaults/main.yml`

```yaml
---
# All variables with defaults
my_role_setting: "default_value"
```

### 4. Create `tasks/main.yml`

```yaml
---
- name: My Role | Display info
  ansible.builtin.debug:
    msg: "Running my role"
  tags: [my-role]

- name: My Role | Do something
  ansible.builtin.module:
    param: "{{ my_role_setting }}"
  tags: [my-role]
```

### 5. Create `handlers/main.yml`

```yaml
---
- name: Restart something
  ansible.builtin.systemd:
    name: something
    state: restarted
  listen: Restart something
```

## Adding a New Repository Format

### 1. Update `repositories.yml`

Add recipe entries for the new format.

### 2. Update `group_vars/all/nexus.yml`

Add format to `nexus_format_blobstore_defaults`.

### 3. Test

```bash
ansible-playbook -i inventories/testing/inventory.yml playbooks/nexus_validate.yml
```

## Running Tests

```bash
# Molecule tests
cd roles/my_role
molecule test

# Lint
ansible-lint roles/my_role

# YAML lint
yamllint roles/my_role
```

## Code Style

- Use 2-space indentation
- Use `ansible.builtin.` prefix for modules
- Use descriptive task names: `Role | Action`
- Tag every task
- Use `loop` instead of `with_items`
- Use `register` for important results
- Use `when` for conditional tasks

## Testing Checklist

- [ ] YAML valid
- [ ] Ansible-lint passes
- [ ] Idempotent (run twice, same result)
- [ ] Check mode works
- [ ] Tags work
- [ ] Variables documented
- [ ] README updated
