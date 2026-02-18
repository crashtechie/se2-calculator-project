# Kiro Configuration Summary

This document provides an overview of the Kiro CLI configuration for the SE2 Calculator Project.

## Directory Structure

```
.kiro/
├── steering/              # Project-specific guidance documents
│   ├── 00-project-overview.md
│   ├── 01-django-standards.md
│   ├── 02-enhancement-workflow.md
│   ├── 03-testing-guidelines.md
│   ├── 04-docker-deployment.md
│   ├── 05-code-style.md
│   ├── 06-resource-chain.md
│   ├── 07-security-secrets.md
│   ├── 08-cicd-github-actions.md
│   └── 09-database-management.md
├── prompts/               # Reusable prompt templates
│   ├── create-enhancement.md
│   ├── write-tests.md
│   ├── review-code.md
│   └── troubleshoot-docker.md
├── tasks/                 # Workflow task definitions
│   ├── new-model.yaml
│   ├── new-view.yaml
│   ├── run-tests.yaml
│   └── deploy-docker.yaml
├── tools/                 # Project-specific utilities
│   ├── validate-fixtures.py
│   ├── check-coverage.sh
│   └── sync-env.sh
├── mcp.json              # MCP server configuration (gitignored)
├── context.json          # Context filtering rules
├── aliases.json          # Command shortcuts
└── MCP_SETUP.md          # MCP setup documentation
```

## Steering Documents (10)

Comprehensive guidance covering:
- Project architecture and standards
- Django development patterns
- Testing and code quality
- Docker deployment
- Security and secrets management
- CI/CD workflows
- Database management

## Prompts (4)

Reusable templates for common tasks:
- **create-enhancement.md** - ENH request creation workflow
- **write-tests.md** - Test writing guidelines and templates
- **review-code.md** - Comprehensive code review checklist
- **troubleshoot-docker.md** - Docker debugging procedures

## Tasks (4)

Structured workflows for:
- **new-model.yaml** - Creating Django models
- **new-view.yaml** - Implementing CRUD views
- **run-tests.yaml** - Test execution workflow
- **deploy-docker.yaml** - Docker deployment checklist

## Tools (3)

Utility scripts:
- **validate-fixtures.py** - Validate fixture UUIDs and structure
- **check-coverage.sh** - Enforce coverage thresholds
- **sync-env.sh** - Sync .env and .env.example

## MCP Servers (5)

Configured servers:
1. **filesystem** ✅ - Enhanced file operations
2. **postgres** ⚙️ - Database queries (needs DB_PASSWORD)
3. **git** ✅ - Git operations and history
4. **github** ⚙️ - GitHub API (needs token)
5. **brave-search** ⚙️ - Web search (needs API key)

See `MCP_SETUP.md` for configuration details.

## Command Aliases (20+)

Quick shortcuts for common commands:
- `test` - Run full test suite with coverage
- `migrate` - Apply database migrations
- `docker-up` - Build and start Docker stack
- `lint` - Check code quality
- `format` - Format code
- And many more...

## Context Filtering

Configured to exclude:
- Cache directories (__pycache__, .pytest_cache, etc.)
- Virtual environments (.venv)
- Build artifacts (staticfiles, dist, build)
- Large files (>100KB)

Auto-includes important files:
- Python source files (app/**/*.py)
- Tests (tests/**/*.py)
- Documentation (docs/**/*.md)
- Configuration files

## Next Steps

### Immediate
1. ✅ Fix .gitignore (completed)
2. ⏳ Initialize LSP: Run `/code init` in Kiro CLI
3. ⏳ Configure MCP credentials in `mcp.json`

### Optional
4. Review and customize steering documents
5. Add project-specific prompts
6. Create additional task workflows
7. Develop custom tools as needed

## Usage Tips

### Using Prompts
Reference prompts in your requests:
- "Follow the create-enhancement prompt to make ENH-0000017"
- "Use the write-tests prompt for the BuildOrder model"

### Using Tasks
Reference tasks for structured workflows:
- "Follow the new-model task to create a Category model"
- "Execute the deploy-docker task"

### Using Tools
Run tools directly:
```bash
python .kiro/tools/validate-fixtures.py
bash .kiro/tools/check-coverage.sh 85
bash .kiro/tools/sync-env.sh
```

### Using Aliases
Use aliases in commands:
- "Run the test alias"
- "Execute docker-up"

## Maintenance

### Regular Updates
- Review steering documents quarterly
- Update prompts as patterns evolve
- Add new tasks for recurring workflows
- Enhance tools based on needs

### Version Control
- Commit steering docs, prompts, tasks, tools
- Never commit mcp.json with credentials
- Keep MCP_SETUP.md updated
- Document changes in CHANGELOG.md

## Support

For questions or issues with Kiro configuration:
1. Review relevant steering document
2. Check MCP_SETUP.md for MCP issues
3. Consult prompt/task templates
4. Update configuration as needed
