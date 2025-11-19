#!/usr/bin/env python3
# Fetch historical chart data for a coin by timeframe (e.g. 1D, 1W) and write to data/raw/

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dropstab_base import RAW_DIR, GET, utc_now_iso, today_tag

COIN_SLUG = "COIN-SLUG-TO-SEARCH"  # e.g. "bitcoin" 

# NOTE:
# - Param name must be exactly "timeFrame" (camelCase), per API error.
# - The value must be one of the supported timeframes (CoinHistorySupportedTimeframe).
#   If the value is invalid, the API will respond with another 400 listing allowed values.
PARAMS = {
    "timeFrame": "DAY",  # adjust to a supported value from the docs UI if needed
    # Optional: "currency": "USD",
}


def main():
    resp = GET(f"coins/history/chart-by-timeframe/{COIN_SLUG}", params=PARAMS)
    data = resp.get("data", resp) if isinstance(resp, dict) else resp

    filename = RAW_DIR / f"coin_chart_timeframe_{COIN_SLUG}_{today_tag()}.json"
    payload = {
        "data_ts_utc": utc_now_iso(),
        "status": "ok",
        "endpoint": "coins/history/chart-by-timeframe/{slug}",
        "slug": COIN_SLUG,
        "query_params": PARAMS,
        "items": data,
    }
    filename.write_text(json.dumps(payload, indent=2))
    print(f"Finished writing {filename}")


if __name__ == "__main__":
    main()
