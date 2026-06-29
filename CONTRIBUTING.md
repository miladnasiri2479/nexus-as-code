# Contributing to Nexus as Code

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

```bash
# Clone
git clone https://github.com/your-username/nexus-as-code.git
cd nexus-as-code

# Install dependencies
pip install ansible-lint yamllint molecule docker

# Install Ansible collections
ansible-galaxy collection install community.docker
ansible-galaxy collection install community.general
ansible-galaxy collection install ansible.posix
```

## Code Style

- 2-space indentation
- Use `ansible.builtin.` prefix
- Tag all tasks
- Document all variables
- Follow [Conventional Commits](https://www.conventionalcommits.org/)

## Testing

```bash
# Lint
ansible-lint
yamllint

# Molecule
cd roles/my_role
molecule test
```

## Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Variables documented
- [ ] Commit messages follow conventions

## License

Apache 2.0
