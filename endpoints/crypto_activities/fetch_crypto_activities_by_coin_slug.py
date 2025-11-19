#!/usr/bin/env python3
# Fetch all crypto activities for a specific coin (paginated) and write to data/raw/

import json
import time
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dropstab_base import RAW_DIR, PAGE_SIZE, SLEEP_SEC, GET, utc_now_iso, today_tag

COIN_SLUG = "COIN-SLUG-TO-SEARCH"  # e.g. "monad" 


def main():
    all_activities = []
    page = 0

    while True:
        params = {"page": page, "pageSize": PAGE_SIZE}
        resp = GET(f"cryptoActivities/coin/{COIN_SLUG}", params=params)
        data = resp.get("data", {}) if isinstance(resp, dict) else {}
        content = data.get("content", [])

        all_activities.extend(content)

        total_pages = data.get("totalPages")
        current_page = data.get("currentPage")

        print(
            f"[cryptoActivities/coin/{COIN_SLUG}] page {current_page}/"
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

    filename = RAW_DIR / f"cryptoActivities_coin_{COIN_SLUG}_{today_tag()}.json"
    payload = {
        "data_ts_utc": utc_now_iso(),
        "status": "ok",
        "endpoint": "cryptoActivities/coin/{coinSlug}",
        "coinSlug": COIN_SLUG,
        "items": all_activities,
    }
    filename.write_text(json.dumps(payload, indent=2))
    print(f"Finished writing {filename} (items: {len(all_activities)})")


if __name__ == "__main__":
    main()
