#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Set UTF-8 encoding for stdout to handle emojis on Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def get_git_branch(cwd):
    """Get current git branch if in a git repo."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=1
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return None

def get_git_stats(cwd):
    """Get git stats: modified files count and line changes since last commit."""
    try:
        # Check if in a git repo
        subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            cwd=cwd,
            capture_output=True,
            timeout=1,
            check=True
        )

        # Get number of modified files (including untracked)
        status_result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=1
        )
        modified_files = len([line for line in status_result.stdout.strip().split('\n') if line])

        # Get line changes since last commit (staged + unstaged)
        diff_result = subprocess.run(
            ['git', 'diff', 'HEAD', '--numstat'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=1
        )

        lines_added = 0
        lines_removed = 0
        for line in diff_result.stdout.strip().split('\n'):
            if line:
                parts = line.split('\t')
                if len(parts) >= 2 and parts[0] != '-' and parts[1] != '-':
                    try:
                        lines_added += int(parts[0])
                        lines_removed += int(parts[1])
                    except:
                        pass

        # Also count lines in untracked files
        untracked_result = subprocess.run(
            ['git', 'ls-files', '--others', '--exclude-standard'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=1
        )

        for untracked_file in untracked_result.stdout.strip().split('\n'):
            if untracked_file:
                try:
                    # Count lines in untracked file
                    with open(Path(cwd) / untracked_file, 'r', encoding='utf-8', errors='ignore') as f:
                        line_count = sum(1 for _ in f)
                        lines_added += line_count
                except:
                    pass

        return modified_files, lines_added, lines_removed
    except:
        pass
    return 0, 0, 0

def compact_path(path, max_length=35):
    """Compact path if too long."""
    # Replace home directory with ~
    home = str(Path.home())
    if path.startswith(home):
        path = '~' + path[len(home):]

    if len(path) <= max_length:
        return path

    parts = Path(path).parts
    if len(parts) <= 2:
        return path

    # For paths starting with ~, keep it
    if path.startswith('~'):
        return f"~{parts[0]}/.../{parts[-1]}"

    return f"{parts[0]}/.../{parts[-1]}"

def create_progress_bar(percentage, width=20):
    """Create a visual progress bar."""
    filled = int(width * percentage / 100)
    empty = width - filled

    # Color coding based on usage
    if percentage >= 90:
        color = "\033[31m"  # Red
    elif percentage >= 75:
        color = "\033[33m"  # Yellow
    else:
        color = "\033[32m"  # Green

    bar = color + "█" * filled + "\033[90m░" * empty + "\033[0m"
    return f"[{bar}]"

def get_ccusage_data():
    """Get usage data from ccusage command."""
    try:
        # On Windows, use npx.cmd; on Unix, use npx
        npx_cmd = 'npx.cmd' if sys.platform == 'win32' else 'npx'

        # Try npx ccusage first, then fall back to ccusage
        commands = [
            [npx_cmd, '-y', 'ccusage@latest', 'blocks', '--json'],
            ['ccusage', 'blocks', '--json']
        ]

        for cmd in commands:
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=15,
                    shell=(sys.platform == 'win32')
                )
                if result.returncode == 0 and result.stdout:
                    # Filter out npm warnings
                    lines = result.stdout.strip().split('\n')
                    json_start = -1
                    for i, line in enumerate(lines):
                        if line.strip().startswith('{'):
                            json_start = i
                            break

                    if json_start >= 0:
                        json_str = '\n'.join(lines[json_start:])
                        data = json.loads(json_str)
                        # Find active block
                        blocks = data.get('blocks', [])
                        for block in blocks:
                            if block.get('isActive'):
                                return block
                        # If no active block, return the most recent non-gap block
                        for block in reversed(blocks):
                            if not block.get('isGap'):
                                return block
            except Exception as e:
                continue
    except:
        pass
    return None

def parse_iso_timestamp(ts_str):
    """Parse ISO timestamp to epoch seconds."""
    try:
        # Handle various ISO formats
        if ts_str.endswith('Z'):
            dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
        else:
            dt = datetime.fromisoformat(ts_str)
        return int(dt.timestamp())
    except:
        return None

def get_max_context(model_name):
    """Get max context window for model."""
    model_lower = model_name.lower()
    if 'opus' in model_lower or 'sonnet' in model_lower or 'haiku' in model_lower:
        return 200000
    return 200000  # Default

def get_context_from_transcript(session_id, project_dir):
    """Read context usage from transcript file."""
    try:
        # Build transcript file path
        transcript_path = Path.home() / '.claude' / 'projects' / f'-{project_dir}' / f'{session_id}.jsonl'

        if not transcript_path.exists():
            return None

        # Read last 20 lines to get latest token count
        with open(transcript_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Parse from the end to find the most recent usage data
        for line in reversed(lines[-20:]):
            try:
                entry = json.loads(line)
                if 'message' in entry and 'usage' in entry.get('message', {}):
                    usage = entry['message']['usage']
                    input_tokens = usage.get('input_tokens', 0)
                    cache_read = usage.get('cache_read_input_tokens', 0)
                    return input_tokens + cache_read
            except:
                continue

    except:
        pass
    return None

def main():
    # Read JSON input from stdin
    data = json.load(sys.stdin)

    # Extract data
    cwd = data.get('cwd', data.get('workspace', {}).get('current_dir', ''))
    model_name = data.get('model', {}).get('display_name', 'Unknown')
    session_id = data.get('session_id', '')

    # Get git info
    git_branch = get_git_branch(cwd)
    modified_files, lines_added, lines_removed = get_git_stats(cwd)

    # LINE 1: Location and environment
    line1_components = []

    # Model (first) - using bright cyan/light blue
    line1_components.append(f"\033[96m[{model_name}]\033[0m")

    # Directory
    dir_display = compact_path(cwd, 35)
    line1_components.append(f"\033[36m📁 {dir_display}\033[0m")

    # Git branch with stats
    if git_branch:
        git_info = f"\033[32m⎇ {git_branch}\033[0m"
        if modified_files > 0:
            git_info += f" \033[37m({modified_files} files, \033[32m+{lines_added}\033[0m/\033[31m-{lines_removed}\033[0m\033[37m)\033[0m"
        line1_components.append(git_info)

    line1 = "   ".join(line1_components)

    # LINE 2: 5-hour window and context usage
    line2_components = []

    # Get usage data from ccusage
    usage_block = get_ccusage_data()

    if usage_block:
        # 5-hour window usage
        total_tokens = usage_block.get('totalTokens', 0)
        reset_time_str = usage_block.get('usageLimitResetTime') or usage_block.get('endTime')
        start_time_str = usage_block.get('startTime')

        # Max plan has 5x larger limits - minimum 50M tokens per 5-hour window
        MAX_PLAN_TOKEN_LIMIT = 38000000

        if reset_time_str and start_time_str:
            start_sec = parse_iso_timestamp(start_time_str)
            reset_sec = parse_iso_timestamp(reset_time_str)
            now_sec = int(datetime.now().timestamp())

            if start_sec and reset_sec:
                # Calculate token usage percentage based on Max plan limit
                token_usage_pct = min(100, int((total_tokens * 100) / MAX_PLAN_TOKEN_LIMIT)) if total_tokens > 0 else 0

                # Calculate time through the window
                total_window = reset_sec - start_sec
                elapsed = now_sec - start_sec
                time_pct = min(100, int((elapsed * 100) / total_window)) if total_window > 0 else 0

                # Calculate time remaining
                remaining = reset_sec - now_sec
                if remaining > 0:
                    hours = remaining // 3600
                    minutes = (remaining % 3600) // 60

                    if hours > 0:
                        time_str = f"{hours}h {minutes}m"
                    else:
                        time_str = f"{minutes}m"

                    # Color code the token percentage
                    if token_usage_pct >= 90:
                        token_color = "\033[31m"  # Red
                    elif token_usage_pct >= 75:
                        token_color = "\033[33m"  # Yellow
                    else:
                        token_color = "\033[32m"  # Green

                    line2_components.append(f"5 hour limit: {token_color}{token_usage_pct}%\033[0m (resets in \033[37m{time_str}\033[0m)")

        # Context window usage from transcript
        max_context = get_max_context(model_name)
        project_dir = cwd.replace('/', '-').replace('\\', '-').replace(':', '-')
        context_tokens = get_context_from_transcript(session_id, project_dir)

        if context_tokens:
            context_pct = min(100, int((context_tokens * 100) / max_context))
            context_bar = create_progress_bar(context_pct, 20)
            line2_components.append(f"Context: {context_bar} \033[37m{context_pct}%\033[0m")
    else:
        # Fallback if ccusage not available
        line2_components.append("\033[90mUsage data unavailable (ccusage not found)\033[0m")

    if line2_components:
        line2 = " \033[90m│\033[0m ".join(line2_components)
        # Output both lines
        print(line1)
        print(line2)
    else:
        # Just output line 1 if no usage data
        print(line1)

if __name__ == '__main__':
    main()
