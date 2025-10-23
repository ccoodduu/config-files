# Claude Code Configuration

## Search & Command Line Tools

Use the right tool for the right job when executing bash commands:

- **Finding FILES?** → Use `fd` (fast file finder)
- **Finding TEXT/strings?** → Use `rg` (ripgrep for text search)
- **Finding CODE STRUCTURE?** → Use `ast-grep` (syntax-aware code search)
- **LISTING FILES/directories?** → Use `ls` (works in bash/WSL environment)
- **SELECTING from multiple results?** → Pipe to `fzf` (interactive fuzzy finder)
- **Interacting with JSON?** → Use `jq` (JSON processor)
- **Interacting with YAML or XML?** → Use `yq` (YAML/XML processor)

### Examples:

```bash
# Find C# files (MUST use --glob flag)
fd --glob "*.cs"

# Find files with depth limit
fd --glob "*.cs" --max-depth 2

# Search for Controller classes in C# files (use --heading to save tokens)
rg "class.*Controller" --type cs --heading

# Search and select interactively
rg "function.*validate" | fzf

# Find C# class patterns with ast-grep
ast-grep run --lang cs -p 'public class $_'

# Find using statements
ast-grep run --lang cs -p 'using $_'

# List files and directories
ls

# Process JSON files
cat package.json | jq '.dependencies'

# Process YAML files (use printf for multi-line)
printf "name: test\nversion: 1.0" | yq '.name'

# Get repo info or check PR status
gh repo view
gh pr list
```

### Installed Tools:

- ✅ **fd** 10.3.0 (MUST use `--glob "pattern"` syntax)
- ✅ **rg** 14.1.1 (ripgrep) - Works perfectly with `--type cs` for C#
- ✅ **ast-grep** 0.39.4 - Use `--lang cs` for C#
- ✅ **fzf** 0.65.1 - Use `--filter` for non-interactive mode
- ✅ **jq** 1.8.1 - JSON processing works perfectly
- ✅ **yq** v4.46.1 - Use `printf` not `echo` for proper YAML formatting
- ✅ **gh** 2.78.0 (GitHub CLI) - Connected and working

### Important Notes:

- **fd**: Always use `--glob "*.ext"` syntax, NOT just `"*.ext"`
- **ast-grep**: Works with C# using `--lang cs`
- **yq**: Use `printf "key: value\nother: data"` for multi-line YAML
- **fzf**: Can work non-interactively with `--filter` option
- **rg**: Always use `--heading` flag to save tokens (shows filename once per file). Use `--type cs` for C# files

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
- **NEVER change the plan or approach mid-implementation without asking first**
- If you discover issues with the current approach, stop and ask before switching to a different solution
- Always get explicit approval before pivoting to a new implementation strategy

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