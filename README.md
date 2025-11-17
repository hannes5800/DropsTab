# DropsTab Data Fetch Scripts

This repository contains a set of small Python scripts to fetch raw data from the [DropsTab](https://dropstab.com/) Pro API and store it as JSON snapshots on disk. The scripts are organized by API domain (coins, token unlocks, funding rounds, investors, etc.) and share a common base module for configuration and HTTP requests.

> Note: Currently only **list-style** endpoints are queried (those returning collections or global history). **Per-entity detail endpoints** (such as `investors/{investorSlug}`, `coins/detailed/{slug}`, `tokenUnlocks/{coinSlug}`, etc.) are intentionally not implemented at this stage.

---

## Project Structure

```text
project-root/
??? DropsTab_API_key.txt       # file with API key (first line)
??? dropstab_base.py           # shared config + HTTP helper
??? run_all_dropstab.py        # convenience runner for all scripts
??? data/
?   ??? raw/                   # JSON snapshots produced by scripts
??? endpoints/
    ??? coins/
    ?   ??? fetch_all_coins.py
    ?   ??? fetch_all_coins_supported.py
    ??? token_unlocks/
    ?   ??? fetch_all_token_unlocks.py
    ?   ??? fetch_all_token_unlocks_supported_coins.py
    ??? funding_rounds/
    ?   ??? fetch_all_funding_rounds.py
    ??? investors/
    ?   ??? fetch_all_investors.py
    ??? history/
    ?   ??? fetch_fear_index_history.py
    ??? crypto_activities/
    ?   ??? fetch_all_crypto_activities.py
    ??? exchanges/
        ??? fetch_all_exchanges.py
