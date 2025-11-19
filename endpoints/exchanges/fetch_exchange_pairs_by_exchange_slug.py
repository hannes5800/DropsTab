#!/usr/bin/env python3
# Fetch all trading pairs for a specific exchange (paginated) and write to data/raw/

import json
import time
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dropstab_base import RAW_DIR, PAGE_SIZE, SLEEP_SEC, GET, utc_now_iso, today_tag

EXCHANGE_SLUG = "EXCHANGE-SLUG-TO-SEARCH"  # e.g. "binance" 


def main():
    all_pairs = []
    page = 0

    while True:
        params = {"page": page, "pageSize": PAGE_SIZE}
        resp = GET(f"exchanges/{EXCHANGE_SLUG}/pairs", params=params)
        data = resp.get("data", {}) if isinstance(resp, dict) else {}
        content = data.get("content", [])

        all_pairs.extend(content)

        total_pages = data.get("totalPages")
        current_page = data.get("currentPage")

        print(
            f"[exchanges/{EXCHANGE_SLUG}/pairs] page {current_page}/"
            f"{(total_pages - 1) if total_pages is not None else '?'} "
            f"with {len(content)} items"
        )

        if (
            not content
            or total_pages is None
            or current_page is None
            or current_page >= total_pages - 1
        ):
            break

        page += 1
        time.sleep(SLEEP_SEC)

    filename = RAW_DIR / f"exchange_pairs_{EXCHANGE_SLUG}_{today_tag()}.json"
    payload = {
        "data_ts_utc": utc_now_iso(),
        "status": "ok",
        "endpoint": "exchanges/{exchangeSlug}/pairs",
        "exchangeSlug": EXCHANGE_SLUG,
        "items": all_pairs,
    }
    filename.write_text(json.dumps(payload, indent=2))
    print(f"Finished writing {filename} (items: {len(all_pairs)})")


if __name__ == "__main__":
    main()
