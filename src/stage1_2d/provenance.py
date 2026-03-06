"""Provenance tracking utilities."""

import subprocess
from typing import Optional


def get_git_sha() -> Optional[str]:
    """Get current git SHA if available.
    
    Returns:
        Git SHA string or None if not in a git repo
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    
    return None


def get_git_status() -> Optional[str]:
    """Get git status (clean or dirty).
    
    Returns:
        "clean" or "dirty" or None if not in a git repo
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            if result.stdout.strip():
                return "dirty"
            else:
                return "clean"
    except Exception:
        pass
    
    return None
