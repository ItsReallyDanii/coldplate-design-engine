"""Provenance tracking for Stage 2 inverse design.

Tracks git status and metadata for reproducibility.
"""

import subprocess
from typing import Optional


def get_git_sha() -> Optional[str]:
    """Get current git commit SHA.
    
    Returns:
        Git SHA string or None if not in git repo
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_git_status() -> str:
    """Get git status (clean or dirty).
    
    Returns:
        'clean', 'dirty', or 'unknown'
    """
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout.strip():
            return 'dirty'
        else:
            return 'clean'
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 'unknown'
