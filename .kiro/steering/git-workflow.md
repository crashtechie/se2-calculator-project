---
inclusion: auto
description: Git workflow and version control best practices including branching strategy, commit guidelines, and PR process
---

# Git Workflow & Version Control Best Practices

## Branch Strategy

### Main Branches
- `main` - Production-ready code, always stable
- `develop` - Integration branch for features

### Feature Branches
- Format: `feature/ENH-XXXXXXX-short-description`
- Example: `feature/ENH-0000010-build-order-views`
- Branch from: `develop`
- Merge to: `develop`

### Bugfix Branches
- Format: `bugfix/issue-number-short-description`
- Example: `bugfix/123-fix-zero-quantity-crash`
- Branch from: `develop` (or `main` for hotfixes)
- Merge to: `develop` (or `main` for hotfixes)

### Hotfix Branches
- Format: `hotfix/version-short-description`
- Example: `hotfix/0.7.1-security-patch`
- Branch from: `main`
- Merge to: `main` AND `develop`

## Commit Guidelines

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependency updates
- `perf`: Performance improvements

### Examples
```
feat(blocks): add component quantity validation

Implement validation to ensure component quantities are positive
integers. Add corresponding tests and update form validation.

Closes #123
```

```
fix(buildorders): prevent crash when quantity is zero

Add validation to reject zero or negative quantities in build orders.
This prevents division by zero errors in resource calculations.

Fixes #456
```

### Commit Best Practices
- Keep commits atomic (one logical change per commit)
- Write clear, descriptive commit messages
- Use present tense ("add feature" not "added feature")
- Reference issue numbers in commit messages
- Separate subject from body with blank line
- Limit subject line to 50 characters
- Wrap body at 72 characters

## Pull Request Process

### Before Creating PR
1. Ensure all tests pass locally
2. Run linting and type checking
3. Update documentation if needed
4. Rebase on latest develop branch
5. Squash WIP commits if appropriate

### PR Title Format
- Follow commit message format
- Example: `feat(blocks): add component quantity validation`

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #123

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
- [ ] Coverage maintained/improved

## Screenshots (if applicable)
```

### PR Review Process
1. Automated checks must pass (CI, tests, linting)
2. At least one approval required
3. Address all review comments
4. Resolve merge conflicts
5. Squash and merge (or rebase and merge)

## Working with Git

### Starting New Work
```bash
# Update local develop branch
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/ENH-0000010-build-order-views

# Make changes and commit
git add .
git commit -m "feat(buildorders): add list view"

# Push to remote
git push -u origin feature/ENH-0000010-build-order-views
```

### Keeping Branch Updated
```bash
# Fetch latest changes
git fetch origin

# Rebase on develop
git checkout feature/your-branch
git rebase origin/develop

# Resolve conflicts if any
# Then continue rebase
git rebase --continue

# Force push (only on feature branches)
git push --force-with-lease
```

### Interactive Rebase (Clean Up Commits)
```bash
# Rebase last 3 commits
git rebase -i HEAD~3

# In editor, choose actions:
# pick = keep commit
# squash = combine with previous
# reword = change commit message
# drop = remove commit
```

## Git Best Practices

### Do's
- Commit early and often
- Write meaningful commit messages
- Keep commits focused and atomic
- Use branches for all changes
- Pull before pushing
- Review your own changes before committing
- Use .gitignore properly

### Don'ts
- Don't commit secrets or credentials
- Don't commit generated files (build artifacts, logs)
- Don't force push to shared branches (main, develop)
- Don't commit commented-out code
- Don't commit debug statements
- Don't mix refactoring with feature changes
- Don't commit broken code

## Handling Merge Conflicts

### Conflict Resolution Steps
1. Identify conflicting files
2. Open files and locate conflict markers
3. Understand both changes
4. Decide which changes to keep
5. Remove conflict markers
6. Test the resolution
7. Commit the merge

### Conflict Markers
```python
<<<<<<< HEAD
# Your changes
code_from_your_branch()
=======
# Their changes
code_from_other_branch()
>>>>>>> branch-name
```

### Tools for Conflict Resolution
- VS Code built-in merge tool
- Git GUI tools (GitKraken, SourceTree)
- Command line: `git mergetool`

## Git Hooks

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run linting
ruff check .
if [ $? -ne 0 ]; then
    echo "Linting failed. Please fix errors before committing."
    exit 1
fi

# Run type checking
mypy .
if [ $? -ne 0 ]; then
    echo "Type checking failed. Please fix errors before committing."
    exit 1
fi

# Run tests
pytest
if [ $? -ne 0 ]; then
    echo "Tests failed. Please fix before committing."
    exit 1
fi
```

### Pre-push Hook
```bash
#!/bin/bash
# .git/hooks/pre-push

# Run full test suite
pytest --cov
if [ $? -ne 0 ]; then
    echo "Tests failed. Push aborted."
    exit 1
fi
```

## Versioning Strategy

### Semantic Versioning (SemVer)
- Format: MAJOR.MINOR.PATCH-PRERELEASE
- Example: 0.7.0-alpha

### Version Bumping Rules
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)
- PRERELEASE: alpha, beta, rc

### Tagging Releases
```bash
# Create annotated tag
git tag -a v0.7.0 -m "Release version 0.7.0"

# Push tag to remote
git push origin v0.7.0

# List all tags
git tag -l
```

## Git Aliases (Productivity Boosters)

Add to `~/.gitconfig`:
```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = log --graph --oneline --all
    amend = commit --amend --no-edit
    undo = reset --soft HEAD~1
```

## Troubleshooting Common Issues

### Undo Last Commit (Keep Changes)
```bash
git reset --soft HEAD~1
```

### Undo Last Commit (Discard Changes)
```bash
git reset --hard HEAD~1
```

### Recover Deleted Branch
```bash
# Find commit hash
git reflog

# Recreate branch
git checkout -b recovered-branch <commit-hash>
```

### Clean Up Local Branches
```bash
# Delete merged branches
git branch --merged | grep -v "\*" | xargs -n 1 git branch -d

# Delete remote-tracking branches that no longer exist
git fetch --prune
```

## GitHub-Specific Features

### Issue Templates
- Create `.github/ISSUE_TEMPLATE/` directory
- Add templates for bugs, features, questions

### PR Templates
- Create `.github/PULL_REQUEST_TEMPLATE.md`
- Standardize PR descriptions

### GitHub Actions
- Automate testing on push
- Run linting and type checking
- Generate coverage reports
- Deploy on merge to main

## Security Considerations

### Sensitive Data
- Never commit passwords, API keys, tokens
- Use environment variables
- Add sensitive files to .gitignore
- Use git-secrets or similar tools

### Scanning for Secrets
```bash
# Install git-secrets
git secrets --install

# Scan repository
git secrets --scan
```

### Removing Committed Secrets
```bash
# Use BFG Repo-Cleaner or git-filter-branch
# Then force push (coordinate with team)
# Rotate compromised credentials immediately
```

## Collaboration Best Practices

### Communication
- Comment on PRs constructively
- Explain reasoning for changes
- Ask questions when unclear
- Acknowledge good work
- Be respectful and professional

### Code Ownership
- Review PRs promptly
- Don't merge your own PRs (unless solo project)
- Get approval from code owners
- Respect team conventions

### Documentation
- Keep README updated
- Document breaking changes
- Update CHANGELOG
- Add migration notes when needed
