import json
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://getfomoapi.fun/api"
API_KEY = os.getenv("FOMO_API_KEY", "").strip()

if not API_KEY:
    raise RuntimeError("FOMO_API_KEY is missing")

session = requests.Session()
session.headers.update(
    {
        "Accept": "application/json",
        "X-API-Key": API_KEY,
    }
)


def api_get(path, params=None, retries=5):
    for attempt in range(retries + 1):
        response = session.get(
            f"{BASE_URL}{path}",
            params=params,
            timeout=30,
        )

        if response.status_code != 429:
            response.raise_for_status()
            return response.json()

        if attempt == retries:
            response.raise_for_status()

        retry_after = response.headers.get("Retry-After", "1")

        try:
            delay = float(retry_after)
        except ValueError:
            delay = 1

        time.sleep(max(delay, 2 ** attempt))

    raise RuntimeError("Request failed")


def get_leaderboard(window="24h", limit=5):
    return api_get(
        f"/leaderboard/{window}",
        params={"limit": limit},
    )


def resolve_wallets(handle):
    result = api_get(f"/users/{handle}")
    trader = result["responseObject"]

    return {
        "id": trader.get("id"),
        "handle": trader.get("userHandle"),
        "displayName": trader.get("displayName"),
        "solana": trader.get("solana"),
        "evm": trader.get("evm"),
    }


def get_swaps(user_id, limit=10, cursor=None):
    params = {"limit": limit}

    if cursor:
        params["cursor"] = cursor

    return api_get(
        f"/users/{user_id}/swaps",
        params=params,
    )


def main():
    leaderboard = get_leaderboard(
        window="24h",
        limit=5,
    )

    print("Leaderboard")
    print(json.dumps(leaderboard, indent=2, ensure_ascii=False))

    traders = leaderboard.get(
        "responseObject",
        {},
    ).get("leaderboard", [])

    if not traders:
        return

    handle = traders[0].get("userHandle")

    if not handle:
        return

    wallets = resolve_wallets(handle)

    print("\nWallets")
    print(json.dumps(wallets, indent=2, ensure_ascii=False))

    user_id = wallets.get("id")

    if not user_id:
        return

    swaps = get_swaps(
        user_id=user_id,
        limit=10,
    )

    print("\nSwaps")
    print(json.dumps(swaps, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
