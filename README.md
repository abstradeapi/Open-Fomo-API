# The Developer API for Fomo Family Social Trading Data

**Fomo API** converts Fomo Family social and onchain trading information into a consistent developer-friendly REST API.

Use trader profiles, verified wallets, leaderboards, balances, holdings, PnL, swaps, and social activity to build:

- Trading dashboards
- Wallet trackers
- Smart-money alerts
- Telegram trading bots
- Copy-trading research tools
- Portfolio analytics
- Automated trading workflows
- AI trading agents

![Image](./docs/img/image.png)

> Fomo API is an independent developer service. It is not an official Fomo Family product and does not provide financial advice.

### Production Services

| Service | URL |
|---|---|
| Website | [https://getfomoapi.fun](https://getfomoapi.fun) |
| Documentation | [https://getfomoapi.fun/docs](https://getfomoapi.fun/docs) |
| Telegram | [@dexlenai](https://t.me/dexlenai) |
| X / Twitter | [@0xdexlenai](https://x.com/0xdexlenai) |

![Image](./docs/img/01.png)

---

## Features

### Social Trading Data

- Resolve Fomo Family handles
- Retrieve trader profiles and social statistics
- Access verified Solana and EVM wallet addresses
- Rank traders across multiple performance windows
- Read balances, token holdings, equity, and PnL
- Retrieve normalized swap history
- Access best trades, comments, and social reactions

![Image](./docs/img/02.png)

### Developer Platform

- Google OAuth authentication
- Secure, account-scoped API keys
- Revealable API keys encrypted at rest
- Five requests per second per API key
- Actual request usage analytics
- Consistent JSON responses
- Interactive API documentation
- Automatic one-hour leaderboard caching


![Image](./docs/img/03.png)


### Solana Payments

- Solana Pay QR code
- Phantom and Solflare support
- USDC payment verification
- Automatic Pro activation
- Transaction replay protection
- Manual USDC transfer detection

---

## Examples:


### Leaderboard

```python
import os

import requests
from dotenv import load_dotenv

load_dotenv()

response = requests.get(
    "https://getfomoapi.fun/api/leaderboard/24h",
    headers={
        "X-API-Key": os.getenv("FOMO_API_KEY"),
    },
    params={
        "limit": 5,
    },
    timeout=30,
)

response.raise_for_status()
leaderboard = response.json()

print(leaderboard)
```

### Resolve Trader Wallets

```python
import os

import requests
from dotenv import load_dotenv

load_dotenv()

handle = "starcatcher444"

response = requests.get(
    f"https://getfomoapi.fun/api/users/{handle}",
    headers={
        "X-API-Key": os.getenv("FOMO_API_KEY"),
    },
    timeout=30,
)

response.raise_for_status()
trader = response.json()["responseObject"]

print("User ID:", trader.get("id"))
print("Solana:", trader.get("solana"))
print("EVM:", trader.get("evm"))
```

### Trader Swaps

```python
import os

import requests
from dotenv import load_dotenv

load_dotenv()

user_id = "254245a7-575a-51be-9bc3-090a924789eb"

response = requests.get(
    f"https://getfomoapi.fun/api/users/{user_id}/swaps",
    headers={
        "X-API-Key": os.getenv("FOMO_API_KEY"),
    },
    params={
        "limit": 10,
    },
    timeout=30,
)

response.raise_for_status()
swaps = response.json()

print(swaps)
```



## API Overview

### Public Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Backend health status |
| `GET` | `/api/health` | Public API health status |
| `GET` | `/plans/pro` | Current Pro plan details |
| `GET` | `/frontpage/leaderboard` | Top five public traders |

![Image](./docs/img/04.png)


### Authentication Endpoints


### API Key Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api-keys` | Generate an API key |
| `GET` | `/api-keys` | List API keys |
| `GET` | `/api-keys/{id}/reveal` | Reveal an encrypted API key |
| `DELETE` | `/api-keys/{id}` | Revoke an API key |

### Pro Data Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/leaderboard/{window}` | Ranked traders |
| `GET` | `/api/users/{handle}` | Resolve a trader |
| `GET` | `/api/users/{userId}/balances` | Balances and positions |
| `GET` | `/api/users/{userId}/spotlight` | Best trades and comments |
| `GET` | `/api/users/{userId}/swaps` | Paginated swaps |
| `GET` | `/api/users/{userId}/leaderboard` | Trader rankings |
| `GET` | `/api/users/current/following-ids` | Followed user IDs |
| `GET` | `/api/user-tokens/aggregated-snapshot` | Historical PnL and equity |

### Planned Realtime Endpoint

```text
WS /ws/trades
```

Realtime trade streaming is documented but not active yet.

---

## Quickstart

### 1. Generate an API Key

Sign in at:

```text
https://getfomoapi.fun/sign-in
```

Open the dashboard and create an API key. Keys begin with:

```text
fomo_live_
```

### 2. Make a Request

```bash
curl "https://getfomoapi.fun/api/leaderboard/24h?limit=5" \
  -H "X-API-Key: fomo_live_YOUR_API_KEY"
```

Bearer authentication is also supported:

```bash
curl "https://getfomoapi.fun/api/leaderboard/24h?limit=5" \
  -H "Authorization: Bearer fomo_live_YOUR_API_KEY"
```

### 3. Read the Response

```json
{
  "success": true,
  "message": "24H Leaderboard found",
  "responseObject": {
    "leaderboard": [
      {
        "id": "254245a7-575a-51be-9bc3-090a924789eb",
        "displayName": "Star Catcher 💫",
        "userHandle": "starcatcher444",
        "solana": "6xmMW5JPSEfeRuNdkxixHWsm4Sf57SdXybA3BdwZzrM1",
        "evm": "0x4bc1782fafb967834e0e75947ba15113e48fc70e",
        "pnl24h": 382726.51,
        "totalVolume": 386307.46
      }
    ]
  },
  "statusCode": 200
}
```

---

## Wallet Resolution

Original wallet fields are normalized into:

```json
{
  "solana": "SOLANA_ADDRESS",
  "evm": "EVM_ADDRESS"
}
```

The wallet resolver:

1. Checks `trader_wallets` for the handle.
2. Returns stored wallets immediately when found.
3. Calls the external wallet finder when missing.
4. Falls back to upstream Fomo wallet fields if necessary.
5. Stores the resolved mapping for future requests.

This reduces external requests and keeps wallet output consistent.

---

## Leaderboard Caching

Each leaderboard window is cached independently:

- `24h`
- `7d`
- `30d`
- `all`

Cached data remains fresh for one hour. After one hour, the next request refreshes the cache.

```text
Request
   │
   ├── Fresh database cache → Return cached response
   │
   └── Missing or expired cache
          │
          ├── Fetch upstream leaderboard
          ├── Resolve wallet mappings
          ├── Save updated response
          └── Return updated response
```

If an upstream refresh fails and an older cache exists, the service may return stale data rather than fail completely.

---

## Authentication and Security

### User Sessions

- Users authenticate through Google OAuth.
- Raw session tokens are stored in HTTP-only cookies.
- Only session token hashes are stored in the database.
- Sessions have configurable expiration.
- Users can revoke the current session or every session.

### API Keys

Each API key has:

- A cryptographic random value
- A SHA-256/HMAC hash used for authentication
- An encrypted copy used for dashboard reveal
- An owner
- A creation timestamp
- A last-used timestamp
- Optional expiration

Never expose API keys in client-side code.

### Rate Limits

Pro keys allow five requests per second.

A limited request returns:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 1
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1
```

Clients should wait for `Retry-After` before retrying.

---


## Responsible Use

> Trading and wallet data may be delayed, incomplete, or incorrect. Always validate important information before making financial decisions.

API consumers are responsible for:

- Protecting API keys
- Respecting rate limits
- Following fair usage requirements
- Validating data before executing trades
- Handling upstream and network errors
- Avoiding abusive scraping or credential sharing

---

## Contact

- Telegram: [@dexlenai](https://t.me/dexlenai)
- X: [@0xdexlenai](https://x.com/0xdexlenai)

