# DropsTab Data Fetch Scripts

This repository contains a set of small Python scripts to fetch raw data from the [DropsTab](https://dropstab.com/) Pro API and store it as JSON snapshots on disk. The scripts are organized by API domain (coins, token unlocks, funding rounds, investors, etc.) and share a common base module for configuration and HTTP requests.

> Note: All **list-style** endpoints (those returning collections or global history) are covered by dedicated scripts. In addition, **single-entity detail and history endpoints** (such as `investors/{investorSlug}`, `coins/detailed/{slug}`, `tokenUnlocks/{coinSlug}`, etc.) are also exposed via small helper scripts that use placeholder IDs/slugs at the top of each file and can be customized as needed.

---

## Project Structure

```text
project-root/
  DropsTab_API_key.txt           # file with API key (first line, not committed)
  dropstab_base.py               # shared config + HTTP helper
  run_all_dropstab.py            # convenience runner for all list-style scripts
  requirements.txt               # Python dependencies
  data/                          # created automatically when running dropstab_base.py, not committed by default
    raw/                         # JSON snapshots produced by scripts
  endpoints/
    coins/
      fetch_all_coins.py
      fetch_all_coins_supported.py
      fetch_coin_details_by_slug.py
    token_unlocks/
      fetch_all_token_unlocks.py
      fetch_all_token_unlocks_supported.py
      fetch_token_unlocks_by_coin_slug.py
      fetch_token_unlocks_chart_by_coin_slug.py
    funding_rounds/
      fetch_all_funding_rounds.py
      fetch_funding_round_details_by_id.py
      fetch_funding_rounds_by_coin_slug.py
    investors/
      fetch_all_investors.py
      fetch_investor_details_by_investor_slug.py
    history/
      fetch_fear_index_history.py
      fetch_coin_price_on_date_by_coin_slug.py
      fetch_coin_chart_by_timeframe_and_coin_slug.py
      fetch_coin_chart_by_interval_and_coin_slug.py
    crypto_activities/
      fetch_all_crypto_activities.py
      fetch_crypto_activity_by_id.py
      fetch_crypto_activities_by_coin_slug.py
    exchanges/
      fetch_all_exchanges.py
      fetch_exchange_details_by_exchange_slug.py
      fetch_exchange_pairs_by_exchange_slug.py
