#!/usr/bin/env python3
"""
Lightweight CI Sanity Check for Nexus-as-Code all.yml configuration.
This ensures no structural drift or obvious misconfigurations break the pipeline.
"""
import yaml
import sys
import os

CONFIG_PATH = "inventories/production/group_vars/all.yml"

def validate_config(file_path):
    if not os.path.exists(file_path):
        print(f"[FAIL] Configuration file missing: {file_path}")
        sys.exit(1)

    try:
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(f"[FAIL] YAML Syntax Error in {file_path}:\n{exc}")
        sys.exit(1)

    errors = []

    # 1. Check Top-Level Keys
    required_keys = ['nexus', 'features', 'storage', 'traefik', 'blobstores', 'repositories']
    for key in required_keys:
        if key not in config:
            errors.append(f"Missing required top-level key: '{key}'")

    # If top-level keys are missing, halt further deep checks to avoid KeyErrors
    if errors:
        return errors

    # 2. Check Nexus Core Variables
    nexus = config.get('nexus', {})
    if not isinstance(nexus.get('admin_user'), str):
        errors.append("nexus.admin_user must be a string")
    if not isinstance(nexus.get('http_port'), int):
        errors.append("nexus.http_port must be an integer")
    if not isinstance(nexus.get('active_realms'), list):
        errors.append("nexus.active_realms must be a list")

    # 3. Feature Flags Consistency
    features = config.get('features', {})
    
    # Storage Validation Logic
    storage = config.get('storage', {})
    if storage.get('type') not in ['file', 's3', 'minio']:
        errors.append("storage.type must be one of: 'file', 's3', 'minio'")

    # Cluster Logic
    cluster_feature = features.get('cluster', {})
    if cluster_feature.get('enabled'):
        if not isinstance(cluster_feature.get('replicas'), int):
            errors.append("features.cluster.replicas must be an integer when cluster is enabled")
        if not nexus.get('db_url'):
            errors.append("nexus.db_url is required when cluster is enabled")

    # Backup Logic
    backup_feature = features.get('backup', {})
    if backup_feature.get('enabled'):
        if not backup_feature.get('schedule'):
            errors.append("features.backup.schedule is required when backup is enabled")
        if backup_feature.get('destination') in ['s3', 'minio'] and not backup_feature.get('bucket'):
            errors.append("features.backup.bucket is required for s3/minio backup destinations")

    # Traefik Logic
    traefik = config.get('traefik', {})
    if traefik.get('enabled') and traefik.get('letsencrypt'):
        if not traefik.get('email'):
            errors.append("traefik.email is required when letsencrypt is enabled")

    return errors

if __name__ == "__main__":
    print(f"Validating {CONFIG_PATH}...")
    validation_errors = validate_config(CONFIG_PATH)

    if validation_errors:
        print("\n[CRITICAL] Configuration validation failed with the following errors:")
        for error in validation_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("\n[OK] Configuration validation passed. Structure and flags are consistent.")
        sys.exit(0)
