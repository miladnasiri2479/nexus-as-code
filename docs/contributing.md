# Contribution Guide

## How to Contribute

### 1. Fork the Repository

```bash
git clone https://github.com/your-username/nexus-as-code.git
cd nexus-as-code
git remote add upstream https://github.com/nexus-as-code/nexus-as-code.git
```

### 2. Create a Branch

```bash
git checkout -b feature/my-feature
```

### 3. Make Changes

- Follow the [Developer Guide](developer.md)
- Add tests for new features
- Update documentation

### 4. Test Your Changes

```bash
# Lint
ansible-lint
yamllint

# Test locally
ansible-playbook -i inventories/testing/inventory.yml playbooks/nexus_deploy.yml --check
```

### 5. Commit

```bash
git add .
git commit -m "feat: add support for XYZ"
```

### 6. Push and Create PR

```bash
git push origin feature/my-feature
```

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation
- `refactor:` — Code refactoring
- `test:` — Tests
- `chore:` — Maintenance

## Code Review

All PRs require review before merge. Reviewers check:

- Code style
- Idempotency
- Documentation
- Test coverage
- Security

## Reporting Issues

Use GitHub Issues with:

- Clear title
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Logs if applicable

## License

By contributing, you agree that your contributions will be licensed under Apache 2.0.
