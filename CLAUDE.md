# Claude Code Configuration

## Search & Command Line Tools

Use the right tool for the right job when executing bash commands:

- **Finding FILES?** → Use `fd` (fast file finder)
- **Finding TEXT/strings?** → Use `rg` (ripgrep for text search)
- **Finding CODE STRUCTURE?** → Use `ast-grep` (syntax-aware code search)
- **SELECTING from multiple results?** → Pipe to `fzf` (interactive fuzzy finder)
- **Interacting with JSON?** → Use `jq` (JSON processor)
- **Interacting with YAML or XML?** → Use `yq` (YAML/XML processor)

### Examples:

```bash
# Find PHP files and interactively select one
fd "*.php" | fzf

# Search for validation functions and select
rg "function.*validate" | fzf

# Find class inheritance patterns
ast-grep --lang php -p 'class $name extends $parent'
```

### Installed Tools:

- ✅ **fd** 10.3.0
- ✅ **rg** 14.1.0 (ripgrep)
- ✅ **sg** 0.39.4 (ast-grep)
- ✅ **fzf** 0.65.1
- ✅ **jq** 1.8.1
- ✅ **yq** v4.46.1
- ✅ **gh** (GitHub CLI)

## Code Style Preferences

### Comments Policy
- Use **minimal comments** - avoid cluttering code with excessive documentation
- Add comments only for complex business logic or non-obvious implementation details
- Prefer explaining code functionality through chat messages rather than inline comments
- Focus on writing self-documenting code with clear variable/function names

### Communication Style
- Explain new code implementations in chat messages instead of code comments
- Provide context and reasoning for design decisions in conversation
- Keep code clean and readable without over-documentation

### Problem-Solving Approach
- **Don't jump to conclusions** - when the solution or next step isn't clear, suggest options first
- Present multiple approaches when ambiguity exists
- Ask for clarification before implementing when requirements are unclear
- Discuss trade-offs and implications before beginning implementation

## GitHub CLI (gh) Commands

### Repository Management
```bash
# Create new repository
gh repo create <name> --public/--private

# Clone repository 
gh repo clone <owner>/<repo>

# View repository details
gh repo view
```

### Issues & Pull Requests
```bash
# Create pull request
gh pr create --title "Title" --body "Description"

# List pull requests
gh pr list

# View PR details
gh pr view <number>

# Create issue
gh issue create --title "Title" --body "Description"

# List issues
gh issue list
```

### Workflow & Actions
```bash
# View workflow runs
gh run list

# View workflow details
gh run view <run-id>

# Re-run failed jobs
gh run rerun <run-id>
```