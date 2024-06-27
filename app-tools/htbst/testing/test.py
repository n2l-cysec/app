import asyncio
import os

from htbst import HTBClient, HTBLabs


async def main():
    client = HTBClient("elliotandmrrobot@ro.ru", os.environ.get("HTB_PASS"))
    sso = await client.run()
    labs = HTBLabs(sso_code=sso)
    print(labs.get_user_progress())


asyncio.run(main())
