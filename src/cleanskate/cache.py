from __future__ import annotations

from pathlib import Path

from platformdirs import user_cache_dir


def default_cache_dir() -> Path:
    """Return the default local cache directory for cleanskate data.

    Returns:
        Path: Per-user cache location for downloaded dataset files.
    """
    return Path(user_cache_dir("cleanskate"))
