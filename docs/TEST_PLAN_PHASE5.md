# QA Test Plan - Phase 5 (High Availability, Scaling & DR)

This document details the Quality Assurance test plan for Phase 5. It covers cluster deployment, dynamic scaling, high-availability failover, and disaster recovery (backups). All validations strictly utilize the REST API with robust retry logic to accommodate distributed system eventual consistency.

---

## 1. Scenario: Cluster Disabled (Default Mode)

**Goal:** Ensure the system defaults to a stable, single-node architecture when clustering is explicitly disabled.

**Execution:**
1. Configure `group_vars/all.yml` with `features.cluster.enabled: false`.
2. Run the playbook.

**Validation (Ansible URI Task):**
```yaml
- name: Validate Single Node API Readiness
  ansible.builtin.uri:
    url: "https://{{ traefik.domain }}/service/rest/v1/status"
    method: GET
    status_code: 200
  register: api_check
  until: api_check.status == 200
  retries: 15
  delay: 10
```
**Expected Result:** Only the `nexus` container exists. API responds successfully.

---

## 2. Scenario: Cluster Enabled (Multi-node)

**Goal:** Verify a multi-node Active-Active deployment behind the Traefik load balancer.

**Execution:**
1. Configure `group_vars/all.yml` with `features.cluster.enabled: true` and `features.cluster.replicas: 3`.
2. Run the playbook.

**Validation (Ansible URI Task):**
```yaml
- name: Validate Cluster API Load Balancing
  ansible.builtin.uri:
    url: "https://{{ traefik.domain }}/service/rest/v1/status"
    method: GET
    status_code: 200
  register: cluster_check
  until: cluster_check.status == 200
  retries: 30
  delay: 5
  # Loop ensures the Load Balancer can serve multiple consecutive requests successfully
  loop: "{{ range(0, 10) | list }}"
```
**Expected Result:** All 3 nodes boot. Traefik round-robins the traffic. 10 consecutive API calls succeed without 502/503 errors.

---

## 3. Scenario: Scaling Up

**Goal:** Verify dynamic addition of nodes without disrupting existing traffic.

**Execution:**
1. Change `features.cluster.replicas: 5`.
2. Run the playbook. While it runs, execute a continuous API polling script.

**Validation:**
- Playbook executes `changed=true` only for the new `nexus-node-4` and `nexus-node-5`.
- Continuous API polling (`GET /service/rest/v1/status`) must NOT drop any requests during the deployment. Traefik automatically routes to the new nodes once their native Docker healthchecks pass.

---

## 4. Scenario: Scaling Down

**Goal:** Verify safe removal of excess nodes.

**Execution:**
1. Change `features.cluster.replicas: 2`.
2. Run the playbook.

**Validation:**
- Nodes 3, 4, and 5 are destroyed (`absent`).
- Nodes 1 and 2 remain untouched.
- API stability check (similar to Scenario 2) must pass immediately after the playbook completes, confirming Traefik safely removed the dead nodes from its pool.

---

## 5. Scenario: Backup Restore

**Goal:** Ensure the system can idempotently restore a tarball backup and recover its state.

**Execution:**
1. Run the playbook with `-e "restore_backup_file=nexus-backup-test.tar.gz"`.

**Validation (Ansible URI Task):**
```yaml
- name: Wait for API Recovery after Restore
  ansible.builtin.uri:
    url: "https://{{ traefik.domain }}/service/rest/v1/status"
    method: GET
    status_code: 200
  register: recovery_check
  until: recovery_check.status == 200
  retries: 60     # Restores take longer to boot
  delay: 10

- name: Validate Restored Configuration State
  ansible.builtin.uri:
    url: "https://{{ traefik.domain }}/service/rest/v1/blobstores"
    method: GET
    user: "admin"
    password: "{{ nexus.admin_password }}"
    force_basic_auth: true
  register: restored_blobstores
  # Check if a known blobstore from the backup exists
  failed_when: "'docker' not in (restored_blobstores.json | map(attribute='name') | list)"
```
**Expected Result:** The container boots with the restored data, and the API validates that the historical configuration (e.g., blobstores) is fully present.

---

## 6 & 7. Scenario: Load Balancer Failover & Node Failure Simulation

**Goal:** Prove High Availability (HA) handles sudden node death gracefully.

**Execution:**
1. Ensure cluster is at `replicas: 3`.
2. Emulate a node crash: `docker kill nexus-node-1`
3. Immediately run the API validation task.

**Validation (Ansible URI Task):**
```yaml
- name: Validate Failover Routing
  ansible.builtin.uri:
    url: "https://{{ traefik.domain }}/service/rest/v1/status"
    method: GET
    status_code: 200
  register: failover_check
  until: failover_check.status == 200
  retries: 5   # Traefik should route around the dead node almost instantly
  delay: 2
  loop: "{{ range(0, 5) | list }}"
```
**Expected Result:** Traefik's active health checks identify `nexus-node-1` is down. Requests are instantly routed to `nexus-node-2` and `nexus-node-3`. The API requests succeed without returning Bad Gateway errors.
