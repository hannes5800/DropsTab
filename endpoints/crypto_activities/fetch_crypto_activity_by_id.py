#!/usr/bin/env python3
# Fetch a single crypto activity by its ID and write to data/raw/

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dropstab_base import RAW_DIR, GET, utc_now_iso, today_tag

ACTIVITY_ID = "ACTIVITY-ID-TO-SEARCH"  # e.g. "1010" 


def main():
    resp = GET(f"cryptoActivities/{ACTIVITY_ID}")
    data = resp.get("data", resp) if isinstance(resp, dict) else resp

    filename = RAW_DIR / f"cryptoActivity_{ACTIVITY_ID}_{today_tag()}.json"
    payload = {
        "data_ts_utc": utc_now_iso(),
        "status": "ok",
        "endpoint": "cryptoActivities/{id}",
        "id": ACTIVITY_ID,
        "items": data,
    }
    filename.write_text(json.dumps(payload, indent=2))
    print(f"Finished writing {filename}")


if __name__ == "__main__":
    main()
