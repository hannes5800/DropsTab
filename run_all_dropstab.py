#!/usr/bin/env python3
"""
Run all DropsTab fetch scripts in sequence.

Usage examples:

    # Run everything
    python run_all_dropstab.py

    # Skip one script
    python run_all_dropstab.py --skip exchanges

    # Skip multiple scripts
    python run_all_dropstab.py --skip exchanges crypto_activities

Available script keys (for --skip):
    funding_rounds
    investors
    coins
    coins_supported
    token_unlocks
    token_unlocks_supported
    fear_index
    crypto_activities
    exchanges
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SCRIPTS = [
    ("funding_rounds", "Funding rounds", "endpoints/funding_rounds/fetch_all_funding_rounds.py"),
    ("investors", "Investors", "endpoints/investors/fetch_all_investors.py"),
    ("coins", "Coins", "endpoints/coins/fetch_all_coins.py"),
    ("coins_supported", "Coins supported", "endpoints/coins/fetch_all_coins_supported.py"),
    ("token_unlocks", "Token unlocks", "endpoints/token_unlocks/fetch_all_token_unlocks.py"),
    (
        "token_unlocks_supported",
        "Token unlocks supported coins",
        "endpoints/token_unlocks/fetch_all_token_unlocks_supported_coins.py",
    ),
    ("fear_index", "Fear index history", "endpoints/history/fetch_fear_index_history.py"),
    ("crypto_activities", "Crypto activities", "endpoints/crypto_activities/fetch_all_crypto_activities.py"),
    ("exchanges", "Exchanges", "endpoints/exchanges/fetch_all_exchanges.py"),
]


def run_script(rel_path: str, label: str) -> None:
    script_path = ROOT / rel_path
    print(f"\n=== Running [{label}] -> {script_path} ===")
    try:
        subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"!!! Script failed: {script_path} (exit code {e.returncode})")
        sys.exit(e.returncode)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run all DropsTab fetch scripts, with optional skipping.",
    )
    parser.add_argument(
        "--skip",
        nargs="+",
        choices=[key for key, _, _ in SCRIPTS],
        default=[],
        help="One or more script keys to skip (see module docstring for list).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    skip_set = set(args.skip)

    if skip_set:
        print(f"Skipping: {', '.join(sorted(skip_set))}")

    print("Starting DropsTab full data fetch...")
    for key, label, rel_path in SCRIPTS:
        if key in skip_set:
            print(f"\n=== Skipping [{label}] ({key}) ===")
            continue
        run_script(rel_path, label)

    print("\nAll selected scripts completed.")


if __name__ == "__main__":
    main()
