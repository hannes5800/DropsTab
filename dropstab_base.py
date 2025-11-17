#!/usr/bin/env python3
"""
Shared configuration and helpers for DropsTab API scripts.

Place this file in your project root next to `DropsTab_API_key.txt`.

Typical usage in endpoint scripts:

    from pathlib import Path
    import sys

    ROOT = Path(__file__).resolve().parents[2]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    from dropstab_base import (
        API_BASE, HEADERS,
        PAGE_SIZE, SLEEP_SEC,
        DATA_DIR, RAW_DIR,
        GET, utc_now_iso, today_tag,
    )
"""

from __future__ import annotations

import time
from pathlib import Path
from datetime import datetime, UTC

import requests


# Paths & directories

# Directory where this file lives => project root
ROOT_DIR = Path(__file__).resolve().parent

# Data directories (shared by all endpoint scripts)
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"

DATA_DIR.mkdir(exist_ok=True)
RAW_DIR.mkdir(exist_ok=True)


# API configuration
API_BASE = "https://public-api.dropstab.com/api/v1"
API_KEY_FILE = ROOT_DIR / "DropsTab_API_key.txt"


def _load_api_key() -> str:
    """
    Load the DropsTab API key from DropsTab_API_key.txt (first non-empty line).

    Raises:
        FileNotFoundError: if the key file is missing.
        RuntimeError: if the file exists but appears to be empty.
    """
    if not API_KEY_FILE.is_file():
        raise FileNotFoundError(
            f"API key file not found: {API_KEY_FILE}. "
            "Create it and put your DropsTab Pro API key in the first line."
        )

    lines = [line.strip() for line in API_KEY_FILE.read_text().splitlines()]
    for line in lines:
        if line:
            return line

    raise RuntimeError(
        f"API key file {API_KEY_FILE} is empty or contains only blank lines."
    )


DT_API_KEY = _load_api_key()

HEADERS = {
    "x-dropstab-api-key": DT_API_KEY,
    "accept": "*/*",
}


# Shared constants

# Default page size for paginated list endpoints (can be overridden per script)
PAGE_SIZE: int = 100

# Default sleep between API calls, in seconds
SLEEP_SEC: float = 0.75


# Time helpers

def utc_now_iso() -> str:
    """Current UTC timestamp in ISO 8601 (seconds precision)."""
    return datetime.now(UTC).isoformat(timespec="seconds")


def today_tag() -> str:
    """Tag for filenames, like '20251116' (UTC date)."""
    return datetime.now(UTC).strftime("%Y%m%d")


# HTTP helper

def GET(path: str, params: dict | None = None, timeout: int = 10):
    """
    Minimal GET helper with one retry on HTTP 429.

    Args:
        path: Either a full URL or a path relative to API_BASE.
        params: Optional query parameters dict.
        timeout: Requests timeout in seconds.

    Returns:
        Parsed JSON (usually a dict), or response text if JSON parsing fails.

    Raises:
        RuntimeError: if the response is not OK (status_code >= 400).
    """
    url = path if path.startswith("http") else f"{API_BASE}/{path.lstrip('/')}"
    params = params or {}

    resp = requests.get(url, headers=HEADERS, params=params, timeout=timeout)

    # Handle rate limiting with a simple single retry.
    if resp.status_code == 429:
        retry_after_raw = resp.headers.get("Retry-After", "2")
        try:
            retry_after = int(retry_after_raw)
        except ValueError:
            retry_after = 2
        time.sleep(retry_after)
        resp = requests.get(url, headers=HEADERS, params=params, timeout=timeout)

    # Try to decode JSON; fall back to raw text
    try:
        payload = resp.json()
    except ValueError:
        payload = resp.text

    if not resp.ok:
        raise RuntimeError(
            f"GET {resp.status_code} :: {url}\n"
            f"Params={params}\n"
            f"Resp={payload}"
        )

    return payload


__all__ = [
    "ROOT_DIR",
    "DATA_DIR",
    "RAW_DIR",
    "API_BASE",
    "API_KEY_FILE",
    "DT_API_KEY",
    "HEADERS",
    "PAGE_SIZE",
    "SLEEP_SEC",
    "utc_now_iso",
    "today_tag",
    "GET",
]
