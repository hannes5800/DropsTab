#!/usr/bin/env python3
# Fetch detailed information about a specific funding round by ID and write to data/raw/

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dropstab_base import RAW_DIR, GET, utc_now_iso, today_tag

FUNDING_ROUND_ID = "FUNDING-ROUND-ID-TO-SEARCH"  # e.g. "16629" 


def main():
    resp = GET(f"fundingRounds/{FUNDING_ROUND_ID}")
    data = resp.get("data", resp) if isinstance(resp, dict) else resp

    filename = RAW_DIR / f"fundingRound_{FUNDING_ROUND_ID}_{today_tag()}.json"
    payload = {
        "data_ts_utc": utc_now_iso(),
        "status": "ok",
        "endpoint": "fundingRounds/{id}",
        "id": FUNDING_ROUND_ID,
        "items": data,
    }
    filename.write_text(json.dumps(payload, indent=2))
    print(f"Finished writing {filename}")


if __name__ == "__main__":
    main()
