#!/usr/bin/env python3
# Fetch full fear index history from DropsTab and write one JSON snapshot to data/raw/

import json
from datetime import datetime, UTC
from pathlib import Path
import sys

# Make project root importable so we can use dropstab_base.py
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dropstab_base import RAW_DIR, GET, utc_now_iso, today_tag

# Use a very early date, without timezone suffix, to effectively get "full history"
FEAR_INDEX_FROM = "2010-01-01T00:00:00"  # must be LocalDateTime (no Z, no offset)


def main():
    # Build "to" as LocalDateTime string (no timezone info)
    to_str = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S")

    params = {
        "from": FEAR_INDEX_FROM,
        "to": to_str,
    }

    resp = GET("coins/history/fear-index", params=params)
    data = resp.get("data", resp) if isinstance(resp, dict) else resp

    filename = RAW_DIR / f"fear_index_history_{today_tag()}.json"
    payload = {
        "data_ts_utc": utc_now_iso(),
        "status": "ok",
        "endpoint": "coins/history/fear-index",
        "query_params": params,
        "items": data,
    }
    filename.write_text(json.dumps(payload, indent=2))

    count = len(data) if hasattr(data, "__len__") else "n/a"
    print(f"Finished writing {filename} (items: {count})")


if __name__ == "__main__":
    main()
