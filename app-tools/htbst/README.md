# unofficial Python library to interact with the Hack The Box API with the newest feature SSO login

## Install

```bash
pip install htbst
```

## Usage

```py
import asyncio
from htbst import HTBClient, HTBLabs

async def main():
    client = HTBClient('elliotandmrrobot@ro.ru', 'my_secure_password')
    sso = await client.run()

asyncio.run(main())
```

## Usage for getting user progress

```py
import asyncio
from htbst import HTBClient, HTBLabs

async def main():
    client = HTBClient('elliotandmrrobot@ro.ru', 'my_secure_password')
    sso = await client.run()
    labs = HTBLabs(sso_code=sso)
    print(labs.get_user_progress())

asyncio.run(main())
```

## Current Features

HTBst provides several features to interact with the Hack The Box API:

### Authentication

* **Email and Password Authentication**: Authenticate users using their Hack The Box email and password to obtain an access token for further API requests.

### Labs Interaction

* **Retrieve User Progress**: Get detailed information about the user's progress in various labs, including machine completions, track progress, and more.

* **Get User Summary**: Fetch a summary of the user's profile, including system owns, user owns, rank, points, and more.

* **Get User Rank Information**: Retrieve detailed information about the user's rank, including current rank, next rank, and season ranking.

### Academy Interaction

[ coming soon ]

### CTF Interaction

[ coming soon ]
