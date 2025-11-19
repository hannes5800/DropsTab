#!/usr/bin/env python3
# Fetch price of a specific coin on a given date (must be in the past) and write to data/raw/

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dropstab_base import RAW_DIR, GET, utc_now_iso, today_tag

COIN_SLUG = "COIN-SLUG-TO-SEARCH"  # e.g. "bitcoin" 
PRICE_DATE = "2024-01-01"          # LocalDate string, format YYYY-MM-DD

PARAMS = {
    "date": PRICE_DATE,
    # Optional: "currency": "USD",
}


def main():
    resp = GET(f"coins/history/price/{COIN_SLUG}", params=PARAMS)
    data = resp.get("data", resp) if isinstance(resp, dict) else resp

    filename = RAW_DIR / f"coin_price_{COIN_SLUG}_{today_tag()}.json"
    payload = {
        "data_ts_utc": utc_now_iso(),
        "status": "ok",
        "endpoint": "coins/history/price/{slug}",
        "slug": COIN_SLUG,
        "query_params": PARAMS,
        "items": data,
    }
    filename.write_text(json.dumps(payload, indent=2))
    print(f"Finished writing {filename}")


if __name__ == "__main__":
    main()
