#!/usr/bin/env python3
# Fetch historical chart data for a coin within a date range (interval) and write to data/raw/

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dropstab_base import RAW_DIR, GET, utc_now_iso, today_tag

COIN_SLUG = "COIN-SLUG-TO-SEARCH"  # e.g. "bitcoin"

# LocalDateTime strings, no timezone suffix (expected type: LocalDateTime)
FROM_DATETIME = "2025-01-01T00:00:00"
TO_DATETIME = "2025-01-31T00:00:00"

# Interval must be one of the supported values (see docs / error message if 400)
INTERVAL = "hour"  # e.g. "hour", "day" (adjust based on docs/options)

PARAMS = {
    "from": FROM_DATETIME,
    "to": TO_DATETIME,
    "interval": INTERVAL,
    # Optional: "currency": "USD",
}


def main():
    resp = GET(f"coins/history/chart-by-interval/{COIN_SLUG}", params=PARAMS)
    data = resp.get("data", resp) if isinstance(resp, dict) else resp

    filename = RAW_DIR / f"coin_chart_interval_{COIN_SLUG}_{today_tag()}.json"
    payload = {
        "data_ts_utc": utc_now_iso(),
        "status": "ok",
        "endpoint": "coins/history/chart-by-interval/{slug}",
        "slug": COIN_SLUG,
        "query_params": PARAMS,
        "items": data,
    }
    filename.write_text(json.dumps(payload, indent=2))
    print(f"Finished writing {filename}")


if __name__ == "__main__":
    main()
