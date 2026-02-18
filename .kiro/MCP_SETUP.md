# MCP Server Configuration Guide

This project uses Model Context Protocol (MCP) servers to extend Kiro's capabilities with specialized tools.

## Configured MCP Servers

### 1. Filesystem Server ✅
**Status**: Ready to use (no configuration needed)

Provides enhanced file system operations scoped to the project directory.

**Capabilities**:
- Advanced file reading and writing
- Directory traversal and search
- File metadata inspection

---

### 2. PostgreSQL Server ⚙️
**Status**: Requires configuration

Enables direct database queries and schema inspection.

**Setup**:
1. Open `.kiro/mcp.json`
2. Set `DB_PASSWORD` in the postgres server's env section
3. Copy password from your `.env` file

```json
"env": {
  "DB_PASSWORD": "your_actual_password_here"
}
```

**Capabilities**:
- Execute SQL queries
- Inspect database schema
- View table contents
- Analyze query performance

**Note**: If using Docker, ensure PostgreSQL port 5432 is exposed to localhost.

---

### 3. Git Server ✅
**Status**: Ready to use (no configuration needed)

Provides Git repository operations and history inspection.

**Capabilities**:
- View commit history
- Inspect branches and tags
- Show file changes and diffs
- Search commit messages
- Analyze repository statistics

---

### 4. GitHub Server ⚙️
**Status**: Requires configuration (optional)

Enables GitHub API access for issues, PRs, and repository management.

**Setup**:
1. Create a GitHub Personal Access Token:
   - Go to https://github.com/settings/tokens
   - Generate new token (classic)
   - Select scopes: `repo`, `read:org`, `read:user`
2. Add token to `.kiro/mcp.json`:

```json
"env": {
  "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_token_here"
}
```

**Capabilities**:
- Create and update issues
- Manage pull requests
- Search repository content
- Access repository metadata
- Manage labels and milestones

**Use Cases**:
- Automated issue creation from bugs
- PR status checking
- Issue tracking and updates
- Repository statistics

---

### 5. Brave Search Server ⚙️
**Status**: Requires configuration (optional)

Provides web search for documentation and technical resources.

**Setup**:
1. Get a Brave Search API key:
   - Go to https://brave.com/search/api/
   - Sign up for API access
2. Add key to `.kiro/mcp.json`:

```json
"env": {
  "BRAVE_API_KEY": "your_api_key_here"
}
```

**Capabilities**:
- Search Django documentation
- Look up Python package docs
- Find Space Engineers 2 game data
- Research technical solutions

**Use Cases**:
- Finding Django best practices
- Looking up library documentation
- Researching game mechanics
- Troubleshooting errors

---

## Activation

After configuring the servers:

1. **Save** `.kiro/mcp.json` with your credentials
2. **Restart** Kiro CLI to load the configuration
3. **Verify** servers are active (they'll appear in available tools)

## Security Notes

- **Never commit** `.kiro/mcp.json` with real credentials to version control
- The file is already in `.gitignore`
- Use environment variables for sensitive values in production
- Rotate tokens regularly (quarterly minimum)

## Troubleshooting

### Server Won't Start
- Check JSON syntax in `mcp.json`
- Verify credentials are correct
- Ensure required services are running (PostgreSQL for postgres server)
- Check Kiro CLI logs for error messages

### PostgreSQL Connection Issues
- Verify database is running: `docker compose ps database`
- Check port forwarding: `docker compose port database 5432`
- Test connection: `psql -h localhost -U se2_user -d se2_calculator`

### GitHub API Rate Limits
- Authenticated requests: 5,000/hour
- Unauthenticated: 60/hour
- Use personal access token to increase limits

## Optional Servers

Additional MCP servers you might consider:

- **Slack**: Team notifications and updates
- **Memory**: Persistent context across sessions
- **Puppeteer**: Web scraping and browser automation
- **Sequential Thinking**: Enhanced reasoning for complex problems

See https://github.com/modelcontextprotocol/servers for more options.
