## Recommended Additional Steering Documents

### 1. Security & Secrets Management
- Environment variable handling
- Secret rotation procedures
- Database credential management
- CSRF/XSS protection patterns
- API key storage best practices

### 2. Performance & Optimization
- Database query optimization patterns
- Caching strategies beyond BuildOrder
- Static file optimization
- N+1 query detection and prevention
- Profiling and benchmarking guidelines

### 3. CI/CD & GitHub Actions
- Workflow troubleshooting procedures
- Test automation standards
- Docker build optimization
- Deployment checklist
- Badge maintenance

### 4. API Development (Future Phase)
- RESTful API conventions
- Serializer patterns
- API versioning strategy
- Rate limiting
- Authentication/authorization

### 5. Frontend Development
- JavaScript/HTMX patterns (if applicable)
- Bootstrap customization guidelines
- Responsive design breakpoints
- Accessibility standards (WCAG)
- Form validation patterns

### 6. Database Management
- Migration best practices
- Fixture creation/maintenance
- Backup/restore procedures
- Data seeding strategies
- PostgreSQL-specific optimizations

## Additional MCP Server Suggestions

### 1. Git MCP Server
json
"git": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-git"]
}

- Enables git operations and history inspection
- Useful for commit analysis and branch management

### 2. GitHub MCP Server
json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": ""
  }
}

- Access issues, PRs, and repository metadata
- Automate issue creation and updates

### 3. Brave Search MCP Server (for documentation lookup)
json
"brave-search": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-brave-search"],
  "env": {
    "BRAVE_API_KEY": ""
  }
}

- Search Django/Python documentation
- Look up Space Engineers 2 game data

## Priority Recommendations

High Priority:
1. Security & Secrets Management - Critical for production readiness
2. CI/CD & GitHub Actions - You have active workflows that need guidance
3. Database Management - Core to your resource chain architecture

Medium Priority:
4. Performance & Optimization - Important as data grows
5. Git MCP Server - Enhances development workflow

Lower Priority (Future):
6. API Development - When you reach Phase 4
7. Frontend Development - If you expand beyond Django templates