# Contributing to Nexus as Code

Welcome to the `nexus-as-code` project! To ensure stability and maintainability, we strictly follow a Git-based development workflow. Please read this document before making any changes.

## 1. Branching Strategy

We use a feature-branch workflow.
- **`main`**: The stable, production-ready branch. **Never push directly to `main`.**
- **Feature Branches**: All development happens here.

### Branch Naming Conventions
Branch names must be descriptive and follow this semantic structure:
- `feature/<description>`: For new features (e.g., `feature/s3-blobstores`).
- `bugfix/<description>`: For bug fixes (e.g., `bugfix/traefik-routing-error`).
- `docs/<description>`: For documentation updates.
- `refactor/<description>`: For code refactoring without behavior changes.

## 2. Commit Message Conventions

We strictly adhere to [Conventional Commits](https://www.conventionalcommits.org/). Every commit message must be structured as follows:

```text
<type>: <short description>
```

**Allowed Types:**
- `feat`: A new feature.
- `fix`: A bug fix.
- `docs`: Documentation only changes.
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc).
- `refactor`: A code change that neither fixes a bug nor adds a feature.
- `chore`: Changes to the build process or auxiliary tools.

## 3. Pull Request (PR) Rules

All changes must be submitted via a Pull Request against the `main` branch. 

Before a PR can be merged, it **MUST**:
1. **Pass CI/CD**: All automated syntax checks and linters (`ansible-lint`, `ansible-playbook --syntax-check`) must pass.
2. **Be Up-to-Date**: The PR branch must be rebased or merged with the latest `main`.
3. **Be Reviewed**: Require at least 1 peer approval.
4. **Squash and Merge**: When merging, all commits in the PR must be squashed into a single, clean commit representing the logical change.

## 4. Developer Workflow Example

```bash
# 1. Sync your local main
git checkout main
git pull origin main

# 2. Create your feature branch
git checkout -b feature/my-awesome-feature

# 3. Make changes, add, and commit
git add .
git commit -m "feat: implement awesome feature"

# 4. Push to remote and open a PR
git push -u origin feature/my-awesome-feature
```
