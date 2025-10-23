# Setup script for Claude Code configuration
# Run this script to set up symlinks and configure the status line

$ErrorActionPreference = "Stop"

Write-Host "Setting up Claude Code configuration..." -ForegroundColor Cyan

# Get paths
$configRepo = $PSScriptRoot
$homeDir = $env:USERPROFILE
$claudeDir = Join-Path $homeDir ".claude"

# Create .claude directory if it doesn't exist
if (-not (Test-Path $claudeDir)) {
    Write-Host "Creating .claude directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $claudeDir -Force | Out-Null
}

# 1. Create symlink for CLAUDE.md in home directory
$claudeMdSource = Join-Path $configRepo "CLAUDE.md"
$claudeMdTarget = Join-Path $homeDir "CLAUDE.md"

if (Test-Path $claudeMdTarget) {
    # Check if it's already a symlink pointing to the right place
    $item = Get-Item $claudeMdTarget
    if ($item.LinkType -eq "SymbolicLink" -and $item.Target -eq $claudeMdSource) {
        Write-Host "CLAUDE.md symlink already exists" -ForegroundColor Green
    } else {
        Write-Host "Removing existing CLAUDE.md..." -ForegroundColor Yellow
        Remove-Item $claudeMdTarget -Force
        New-Item -ItemType SymbolicLink -Path $claudeMdTarget -Target $claudeMdSource | Out-Null
        Write-Host "Created CLAUDE.md symlink" -ForegroundColor Green
    }
} else {
    New-Item -ItemType SymbolicLink -Path $claudeMdTarget -Target $claudeMdSource | Out-Null
    Write-Host "Created CLAUDE.md symlink" -ForegroundColor Green
}

# 2. Create symlink for statusline.py in .claude directory
$statuslineSource = Join-Path $configRepo "statusline.py"
$statuslineTarget = Join-Path $claudeDir "statusline.py"

if (Test-Path $statuslineTarget) {
    $item = Get-Item $statuslineTarget
    if ($item.LinkType -eq "SymbolicLink" -and $item.Target -eq $statuslineSource) {
        Write-Host "statusline.py symlink already exists" -ForegroundColor Green
    } else {
        Write-Host "Removing existing statusline.py..." -ForegroundColor Yellow
        Remove-Item $statuslineTarget -Force
        New-Item -ItemType SymbolicLink -Path $statuslineTarget -Target $statuslineSource | Out-Null
        Write-Host "Created statusline.py symlink" -ForegroundColor Green
    }
} else {
    New-Item -ItemType SymbolicLink -Path $statuslineTarget -Target $statuslineSource | Out-Null
    Write-Host "Created statusline.py symlink" -ForegroundColor Green
}

# 3. Update settings.json to use the status line
$settingsPath = Join-Path $claudeDir "settings.json"

# Create proper JSON manually to avoid PowerShell formatting issues
$escapedPath = $statuslineTarget -replace '\\', '\\'
$settingsJson = @"
{
  "alwaysThinkingEnabled": false,
  "statusLine": {
    "type": "command",
    "command": "python $escapedPath",
    "padding": 0
  }
}
"@

# Write settings with proper encoding (UTF-8 without BOM)
[System.IO.File]::WriteAllText($settingsPath, $settingsJson)
Write-Host "Updated settings.json with statusline configuration" -ForegroundColor Green

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Your configuration is now synced with: $configRepo" -ForegroundColor Cyan
Write-Host "Restart Claude Code to see your custom status line." -ForegroundColor Yellow
