# QA Test Plan - Phase 2 (Nexus Bootstrap)

This document details the Quality Assurance test plan specifically for Phase 2 of the Nexus as Code project (`nexus_bootstrap` role). The focus is on API interaction, authentication, security hardening, and idempotency.

---

## 1. Fresh Deployment Scenario

**Goal:** Validate that a newly deployed Nexus instance is successfully bootstrapped and secured automatically.

**Prerequisites:**
- Phase 1 completed (Nexus container is running for the first time).
- Default auto-generated password file exists in `/opt/nexus-data/admin.password`.

**Execution:**
1. Run the configure playbook targeting Phase 2:
   ```bash
   ansible-playbook -i inventories/production/hosts.yml playbooks/site.yml --tags "bootstrap"
   ```

**Expected Outputs:**
- Task `Wait for Nexus API to be accessible` passes.
- Task `Retrieve initial admin password from container volume` reads the file successfully.
- Task `Change admin password using API` executes with `changed=true`.
- Anonymous access is disabled (`changed=true`).
- Security realms (DockerToken, NexusAuthenticatingRealm) are enabled (`changed=true`).
- **Post-Deployment Validation:** All validation assertions pass successfully (`[OK] Validation Passed...`).

---

## 2. Re-run Scenario (Idempotency)

**Goal:** Ensure the playbook can be safely executed multiple times without making unnecessary API calls or failing.

**Prerequisites:**
- Scenario 1 completed successfully.

**Execution:**
1. Execute the exact same playbook command again:
   ```bash
   ansible-playbook -i inventories/production/hosts.yml playbooks/site.yml --tags "bootstrap"
   ```

**Expected Outputs:**
- The task `Check if admin password is already configured` returns HTTP 200 (Success).
- Task `Change admin password using API` is **skipped**.
- Tasks for updating Anonymous Access and Security Realms are evaluated but return `ok` (changed=0) because the state matches the desired configuration.
- **Post-Deployment Validation:** Passes instantly.
- **Play Recap:** `changed=0` for the entire `nexus_bootstrap` role.

---

## 3. API Delay Scenario

**Goal:** Test the resilience of the playbook against a slow-starting Nexus instance.

**Prerequisites:**
- Restart the Nexus container immediately before running the playbook to simulate a cold boot delay.
  ```bash
  docker restart nexus
  ```

**Execution:**
1. Immediately run the playbook:
   ```bash
   ansible-playbook -i inventories/production/hosts.yml playbooks/site.yml --tags "bootstrap"
   ```

**Expected Outputs:**
- The `Wait for Nexus API to be accessible` task will poll the `/service/rest/v1/status` endpoint.
- It will safely retry (showing "FAILED - RETRYING" in Ansible output temporarily) up to 30 times with a 5-second delay.
- Once Nexus finishes initializing (usually within 1-2 minutes), the task registers as `ok` and the playbook resumes normal execution.
- No false failures or broken states occur.

---

## 4. Failure Recovery Scenario

**Goal:** Ensure the playbook fails gracefully and provides actionable errors when external factors break the system contract.

**Execution A: Invalid Credentials (Tampered State)**
1. Manually change the `admin` password via the Nexus UI to something random (e.g., `Tampered123!`).
2. Run the playbook with the desired password in `group_vars` (e.g., `SuperSecretPassword123!`).

**Expected Output A:**
- The playbook attempts to authenticate with `SuperSecretPassword123!` and receives a 401 Unauthorized.
- It attempts to read `/opt/nexus-data/admin.password` (which was deleted by Nexus after the first change) and fails.
- Playbook halts gracefully, preventing further configuration drift.
- **Validation:** Administrator must update `group_vars` to match the tampered password or reset the Nexus instance.

**Execution B: Desired State Drift**
1. Manually enable Anonymous Access via the Nexus UI.
2. Run the playbook again.

**Expected Output B:**
- The playbook detects the drift.
- Task `Update anonymous access` executes and returns `changed=true`.
- **Validation:** The post-deployment validation confirms Anonymous access has been forced back to `disabled` (or the desired state in `group_vars`).
