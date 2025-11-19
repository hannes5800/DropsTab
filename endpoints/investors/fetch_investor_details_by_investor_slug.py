#!/usr/bin/env python3
# Fetch detailed information about a specific investor or VC by slug and write to data/raw/

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dropstab_base import RAW_DIR, GET, utc_now_iso, today_tag

INVESTOR_SLUG = "INVESTOR-SLUG-TO-SEARCH"  # e.g. "jump-trading" 


def main():
    resp = GET(f"investors/{INVESTOR_SLUG}")
    data = resp.get("data", resp) if isinstance(resp, dict) else resp

    filename = RAW_DIR / f"investor_{INVESTOR_SLUG}_{today_tag()}.json"
    payload = {
        "data_ts_utc": utc_now_iso(),
        "status": "ok",
        "endpoint": "investors/{investorSlug}",
        "investorSlug": INVESTOR_SLUG,
        "items": data,
    }
    filename.write_text(json.dumps(payload, indent=2))
    print(f"Finished writing {filename}")


if __name__ == "__main__":
    main()
