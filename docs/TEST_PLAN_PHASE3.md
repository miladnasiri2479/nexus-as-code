# QA Test Plan - Phase 3 (Storage & Repositories)

This document details the Quality Assurance test plan for Phase 3 of the Nexus as Code project. This phase focuses on the dynamic provisioning of `storage` validation, `nexus_blobstores`, and `nexus_repositories`.

---

## 1. Scenario: Default File Storage

**Goal:** Verify that local file-based storage and repositories are created successfully when no external storage is configured.

**Execution:**
1. Configure `group_vars/all.yml` with `storage.type: "file"`.
2. Enable `docker_hub` and `maven_central` in the `repositories` dictionary.
3. Run the playbook: `ansible-playbook -i inventories/production/hosts.yml playbooks/site.yml`

**Expected Results:**
- The `storage` role safely skips AWS/MinIO credential validation and logs `[INFO] Storage type is 'file'`.
- `nexus_blobstores` successfully `POST`s file-based blobstore payloads.
- `nexus_repositories` creates proxy repositories bound to the local blobstores.
- **Validation:** Running a `GET` against `/service/rest/v1/blobstores` shows the blobstores with type `File`.

---

## 2. Scenario: S3 Enabled

**Goal:** Verify seamless integration with AWS S3 using standard credentials.

**Execution:**
1. Configure `group_vars/all.yml` with `storage.type: "s3"`, a valid `bucket`, `region`, `access_key`, and `secret_key`.
2. Run the playbook.

**Expected Results:**
- The `storage` role natively validates the AWS S3 bucket existence and IAM permissions.
- `nexus_blobstores` provisions S3 blobstores in Nexus, utilizing the blobstore name as the bucket `prefix`.
- `nexus_repositories` correctly binds to these S3 blobstores.
- **Validation:** Upload a dummy artifact to Nexus and verify it appears in the AWS S3 console under the specified bucket and prefix.

---

## 3. Scenario: MinIO Enabled

**Goal:** Verify S3-compatible (MinIO) backend provisioning using custom endpoints and path-style access.

**Execution:**
1. Configure `group_vars/all.yml` with `storage.type: "minio"`, a valid `endpoint` (e.g., `http://minio:9000`), `bucket`, and credentials.
2. Run the playbook.

**Expected Results:**
- The `storage` role validates the custom endpoint and bucket.
- `nexus_blobstores` automatically injects `forcePathStyle: true` into the S3 payload (which is mandatory for MinIO).
- **Validation:** Check the Nexus UI Administration -> Blob Stores. The Advanced Connection settings should show the custom endpoint and "Force Path Style" checked.

---

## 4. Scenario: Invalid Credentials (Failure Case)

**Goal:** Ensure the system fails fast and protects Nexus from being misconfigured with broken external storage.

**Execution:**
1. Set `storage.type: "s3"` or `"minio"` with deliberately incorrect `access_key` or `secret_key`.
2. Run the playbook.

**Expected Results:**
- The `storage` role attempts to validate the bucket.
- The `Assert Bucket is Accessible` task **fails immediately**.
- Ansible halts execution.
- **Validation:** `nexus_blobstores` and `nexus_repositories` are skipped entirely. Nexus remains untouched and stable.

---

## 5. Scenario: Nexus Restart During Provisioning

**Goal:** Test the resilience of the API calls if the Nexus service drops mid-execution.

**Execution:**
1. Start the playbook with multiple repositories enabled.
2. While `nexus_repositories` is executing, manually restart the Nexus container in another terminal: `docker restart nexus`.

**Expected Results (Failure Case):**
- The Ansible `uri` task currently executing will fail with a `Connection Refused` or `Timeout` error.
- Playbook halts.
**Recovery Validation:**
- Wait for Nexus to boot back up.
- Re-run the playbook. Because the roles are strictly idempotent (checking state with `GET` before `POST`/`PUT`), the playbook will flawlessly resume, skipping the repos already created, and creating the missing ones.

---

## 6. Scenario: Re-run Idempotency Test

**Goal:** Verify that Phase 3 makes zero changes when the desired state is already met.

**Execution:**
1. Ensure Scenario 1, 2, or 3 has completed successfully.
2. Re-run the exact same playbook without modifying `group_vars/all.yml`.

**Expected Results:**
- `storage` role returns `ok`.
- `nexus_blobstores` evaluates existing stores and returns `changed=0`.
- `nexus_repositories` evaluates existing repos and returns `changed=0`.
- **Validation:** The Ansible play recap shows `changed=0` for Phase 3. No blobstores or repositories were deleted or recreated.
