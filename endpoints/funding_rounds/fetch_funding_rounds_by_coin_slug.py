#!/usr/bin/env python3
# Fetch all funding rounds for a specific coin (paginated) and write to data/raw/

import json
import time
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dropstab_base import RAW_DIR, PAGE_SIZE, SLEEP_SEC, GET, utc_now_iso, today_tag

COIN_SLUG = "COIN-SLUG-TO-SEARCH"  # e.g. "the-graph"


def main():
    resp = GET(f"fundingRounds/coin/{COIN_SLUG}")
    # unwrap common API pattern: {"data": [...]} or just [...]
    data = resp.get("data", resp) if isinstance(resp, dict) else resp

    # Ensure we always have a list for "items"
    items = data if isinstance(data, list) else [data]

    filename = RAW_DIR / f"fundingRounds_coin_{COIN_SLUG}_{today_tag()}.json"
    payload = {
        "data_ts_utc": utc_now_iso(),
        "status": "ok",
        "endpoint": "fundingRounds/coin/{coinSlug}",
        "coinSlug": COIN_SLUG,
        "items": items,
    }
    filename.write_text(json.dumps(payload, indent=2))
    print(f"Finished writing {filename} (items: {len(items)})")


if __name__ == "__main__":
    main()
