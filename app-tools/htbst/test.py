import asyncio
from htbst import HTBClient, HTBLabs

async def main():
    client = HTBClient('elliotandmrrobot@ro.ru', 'ur-pass')
    sso = await client.run()
    labs = HTBLabs(sso_code=sso)
    print(labs.get_user_progress())
    
asyncio.run(main())