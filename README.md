# Claude Code Configuration

Personal Claude Code configuration files synced across devices.

## Contents

- `CLAUDE.md` - Claude Code project instructions and preferences
- `statusline.py` - Custom status line script showing:
  - Model name in brackets
  - Current directory (with `~` for home)
  - Git branch with file/line change stats (includes untracked files)
  - 5-hour token limit usage (configured for Max plan: 50M tokens)
  - Time until limit reset

## Setup

### Windows

Run the setup script with administrator privileges (required for creating symlinks):

```powershell
cd ~/config-files
powershell -ExecutionPolicy Bypass -File setup.ps1
```

Or right-click `setup.ps1` and select "Run with PowerShell" (as Administrator).

### Manual Setup

If you prefer to set up manually:

1. Create symlink for CLAUDE.md:
   ```powershell
   New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\CLAUDE.md" -Target "$env:USERPROFILE\config-files\CLAUDE.md"
   ```

2. Create symlink for statusline.py:
   ```powershell
   New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\statusline.py" -Target "$env:USERPROFILE\config-files\statusline.py"
   ```

3. Update `~/.claude/settings.json` to include:
   ```json
   {
     "statusLine": {
       "type": "command",
       "command": "python C:\\Users\\YourUsername\\.claude\\statusline.py",
       "padding": 0
     }
   }
   ```

4. Restart Claude Code

## Requirements

- Python 3.x installed and in PATH
- Git (for git-aware features)
- `npx` (Node.js) for ccusage integration
- Claude Code Max plan (script configured for 50M token limit)

## Status Line Features

**Line 1:** [Model Name]   📁 directory   ⎇ branch (X files, +Y/-Z)

**Line 2:** 5 hour limit: XX% (resets in Xh Xm)

### Color Coding

- **Model**: Bright cyan
- **Directory**: Cyan
- **Git branch**: Green
- **Git stats**: White with green (+) and red (-)
- **Token usage**:
  - Green (0-74%)
  - Yellow (75-89%)
  - Red (90-100%)
- **Reset time**: White

## Updating

After pulling changes from the repo, restart Claude Code to apply updates.

## Notes

- The status line uses `ccusage` via npx to track the 5-hour rolling window
- Git stats include untracked files
- Token limit is set to 50M for Max plan users (adjust in `statusline.py` if needed)
