# QA Test Plan - Phase 4 (Edge Routing & Security Hardening)

This document details the Quality Assurance test plan specifically for Phase 4 of the Nexus as Code project (`traefik` and `security_hardening` roles). The focus is on validating external exposure, TLS termination, routing correctness, and ensuring internal endpoints remain protected.

---

## 1. Automated Validation Suite (Ansible Tasks)

To automate the validation of Phase 4, the following Ansible tasks should be executed from a machine *outside* the target environment to test the externally visible behavior.

```yaml
---
# qa_validation_phase4.yml
- name: Phase 4 Validation Suite
  hosts: localhost
  gather_facts: false
  vars:
    nexus_domain: "nexus.mycompany.local" # Replace with actual domain
    target_ip: "192.168.1.100"            # Replace with actual IP

  tasks:
    - name: 1 & 2. Check HTTP to HTTPS Redirection
      ansible.builtin.uri:
        url: "http://{{ nexus_domain }}"
        method: GET
        status_code: 301 # Traefik default redirect status
        follow_redirects: none
      register: http_redirect
      until: http_redirect.status == 301
      retries: 5
      delay: 5

    - name: 3. Verify Traefik Routing works correctly (HTTPS)
      ansible.builtin.uri:
        url: "https://{{ nexus_domain }}/"
        method: GET
        status_code: 200
        validate_certs: false # Set to true if using real Let's Encrypt, false for local testing/self-signed
      register: https_route
      until: https_route.status == 200
      retries: 10
      delay: 5

    - name: 5. Verify Nexus API is accessible via proxy
      ansible.builtin.uri:
        url: "https://{{ nexus_domain }}/service/rest/v1/status"
        method: GET
        status_code: 200
        validate_certs: false
      register: api_proxy_check
      until: api_proxy_check.status == 200
      retries: 5
      delay: 5

    - name: 6. Check for direct Port 8081 exposure (Must Fail)
      ansible.builtin.wait_for:
        host: "{{ target_ip }}"
        port: 8081
        state: started
        timeout: 5
      ignore_errors: true
      register: port_exposure_check

    - name: Assert no direct exposure
      ansible.builtin.assert:
        that:
          - port_exposure_check.failed == true
        fail_msg: "[CRITICAL] Nexus internal port 8081 is directly exposed to the network!"
        success_msg: "[OK] Nexus port 8081 is securely hidden behind the proxy."
```

---

## 2. Manual Scenarios

### Scenario A: TLS Certificate Validation (Check #4)
**Goal:** Ensure the certificate issued by Traefik is valid and matches the domain.
**Execution:**
1. From an external machine, run:
   ```bash
   echo | openssl s_client -showcerts -connect <nexus_domain>:443 2>/dev/null | openssl x509 -inform pem -noout -text | grep -A 1 "Subject Alternative Name"
   ```
**Expected Output:**
- The output should display the domain `DNS:<nexus_domain>`.
- If using Let's Encrypt (in production), the issuer should be `C = US, O = Let's Encrypt, CN = R3` (or similar).

### Scenario B: HTTP Redirection Loop Testing
**Goal:** Ensure trailing slashes or sub-paths correctly redirect to HTTPS without breaking.
**Execution:**
1. Run `curl -IL http://<nexus_domain>/repository/maven-public/`
**Expected Output:**
- First response: `HTTP/1.1 301 Moved Permanently` (Location: `https://...`)
- Second response: `HTTP/2 200 OK` or `401 Unauthorized` (depending on repo auth, but NEVER a 404 from Traefik).

---

## 3. Failure Recovery Scenarios

**Goal:** Ensure the proxy layer recovers from upstream failures.

**Execution:**
1. Stop the Nexus container manually: `docker stop nexus`
2. Access `https://<nexus_domain>`
**Expected Output:**
- Traefik should return a `502 Bad Gateway` gracefully.
**Recovery:**
3. Start the Nexus container: `docker start nexus`
4. Access `https://<nexus_domain>` again.
**Expected Output:**
- Traefik automatically routes traffic back to Nexus as soon as the container is healthy (no Traefik restart required due to dynamic configuration).
