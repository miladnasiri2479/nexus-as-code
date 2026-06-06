# QA Test Plan - Idempotency & Reconciliation

This test plan validates the core declarative nature of the `nexus-as-code` project. It ensures that the Ansible playbooks act as a true reconciliation engine, applying only delta changes and gracefully recovering from external mutations without generating duplicates or errors.

---

## 1. Scenario: Run system first time (Greenfield)

**Goal:** Establish the initial baseline state.

**Execution:**
1. Start with a pristine environment (no Docker containers, no Nexus data).
2. Configure `inventories/production/group_vars/all.yml` with a standard set of features (e.g., 2 repositories enabled, S3 storage disabled).
3. Run the main playbook:
   ```bash
   ansible-playbook -i inventories/production/hosts.yml playbooks/site.yml
   ```

**Expected Results:**
- All enabled roles execute.
- Play recap shows multiple tasks marked as `changed`.
- No tasks report `failed`.
- Nexus is accessible and fully configured per `all.yml`.

---

## 2. Scenario: Run system second time (No Changes)

**Goal:** Prove strict idempotency. A second run against an identical desired state must result in zero mutations.

**Execution:**
1. Do not modify `all.yml` or the Nexus UI.
2. Run the main playbook immediately after Scenario 1 completes:
   ```bash
   ansible-playbook -i inventories/production/hosts.yml playbooks/site.yml
   ```

**Expected Results:**
- Playbook executes much faster.
- **CRITICAL:** The Ansible Play Recap must show exactly `changed=0`.
- All mutative tasks (`POST`, `PUT`, `DELETE` via URI, or `docker_container`) report as `ok` (green) or are gracefully skipped.
- No duplicate blobstores or repositories are created.

---

## 3. Scenario: Modify config slightly (Delta Update)

**Goal:** Verify the engine detects configuration changes and applies *only* the delta, without destroying unchanged resources.

**Execution:**
1. Edit `inventories/production/group_vars/all.yml`.
2. Change the `admin_password` to a new secure string.
3. Enable a new repository (e.g., set `npm_registry.enabled: true`).
4. Run the main playbook.

**Expected Results:**
- The task for `Change admin password using API` executes (`changed=true`).
- The task `Create Repository` executes **only** for `npm-proxy-registry` (`changed=true`).
- Existing repositories (e.g., Docker, Maven) evaluate to `ok` and are **not** recreated or duplicated.
- The Play Recap shows `changed=2` (or however many exact deltas were introduced).

---

## 4. Scenario: Remove resource manually from Nexus (Drift)

**Goal:** Simulate external tampering and verify the drift detection tool works.

**Execution:**
1. Log into the Nexus Web UI as an administrator.
2. Manually delete the `docker-proxy-hub` repository.
3. Manually enable "Anonymous Access" in the security settings.
4. Run the drift audit playbook:
   ```bash
   ansible-playbook -i inventories/production/hosts.yml playbooks/drift_audit.yml
   ```

**Expected Results:**
- The audit playbook completes with `changed=0` (read-only execution).
- The output displays a `DRIFT DETECTION REPORT` containing two items:
  - `Security: Anonymous Access` (Severity: CRITICAL)
  - `Repository: docker-proxy-hub` (Severity: MEDIUM, Actual: Missing)

---

## 5. Scenario: Re-run system (Self-Healing)

**Goal:** Verify the system can autonomously repair the drift introduced in Scenario 4 without failing.

**Execution:**
1. Run the main playbook to enforce the desired state:
   ```bash
   ansible-playbook -i inventories/production/hosts.yml playbooks/site.yml
   ```

**Expected Results:**
- The `Update anonymous access` task executes (`changed=true`), disabling it again.
- The `Create Repository` task detects the missing `docker-proxy-hub` and executes a `POST` request (`changed=true`).
- **Validation:** Running the drift audit playbook (`drift_audit.yml`) immediately afterward reports `[OK] No configuration drift detected`.
- No errors or duplicate entries occur.
