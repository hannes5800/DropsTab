#!/usr/bin/env python3
# Fetch all coins with token unlock data from DropsTab and write one JSON snapshot to data/raw/

import json
import time
from pathlib import Path
import sys

# Make project root importable so we can use dropstab_base.py
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dropstab_base import RAW_DIR, PAGE_SIZE, SLEEP_SEC, GET, utc_now_iso, today_tag


def main():
    all_supported = []
    page = 0  # currentPage is 0-indexed per docs

    while True:
        params = {"page": page, "pageSize": PAGE_SIZE}
        resp = GET("tokenUnlocks/supportedCoins", params=params)
        data = resp.get("data", {}) if isinstance(resp, dict) else {}
        content = data.get("content", [])

        all_supported.extend(content)

        total_pages = data.get("totalPages")
        current_page = data.get("currentPage")

        print(
            f"[tokenUnlocks/supportedCoins] page {current_page}/"
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

    filename = RAW_DIR / f"tokenUnlocks_supportedCoins_all_{today_tag()}.json"
    payload = {
        "data_ts_utc": utc_now_iso(),
        "status": "ok",
        "endpoint": "tokenUnlocks/supportedCoins",
        "items": all_supported,
    }
    filename.write_text(json.dumps(payload, indent=2))
    print(f"Finished writing {filename} (items: {len(all_supported)})")


if __name__ == "__main__":
    main()
