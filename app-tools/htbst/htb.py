from typing import Optional, Tuple
import httpx
import asyncio

API_BASE = "https://account.hackthebox.com"
LABS_BASE = "https://labs.hackthebox.com"

class HTBClient:
    """
    A client for interacting with Hack The Box's API to authenticate a user and retrieve an access token for the labs.

    Attributes:
        email (Optional[str]): The email address of the user.
        password (Optional[str]): The password of the user.
        api_base (str): The base URL for the Hack The Box API.
    """
    def __init__(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        api_base: str = API_BASE,
    ):
        self.client = httpx.AsyncClient(base_url=api_base, headers={'Accept': 'application/json'})
        self.api_base = api_base
        self.email = email
        self.password = password

    async def initialize(self) -> Tuple[httpx.Cookies, str]:
        """
        Initialize the client by retrieving CSRF cookies.

        Returns:
            Tuple[httpx.Cookies, str]: A tuple containing the cookies and the CSRF token.
        """
        response = await self.client.get('/api/v1/csrf-cookie')
        self.cookies = response.cookies
        self.csrf_token = response.cookies["XSRF-TOKEN"].replace("%3D", "=")
        return self.cookies, self.csrf_token
    
    async def do_login(self) -> httpx.Cookies:
        """
        Authenticate the user using the provided email and password.
        
        Returns:
            httpx.Cookies: a logged cookies.
        """
        response = await self.client.post(
            '/api/v1/auth/login',
            json={
                "email": self.email,
                "password": self.password,
                "remember": True,
            },
            headers={
                "X-Xsrf-Token": self.csrf_token,
                "Referer": f"{API_BASE}/login",
            },
            cookies=self.cookies
        )
        self.logged_cookies = response.cookies
        return self.logged_cookies
    
    async def labs(
        self,
        logged_cookies: Optional[str] 
    ):
        """Initiate the SSO process and retrieve the SSO code."""
        if logged_cookies:
            self.logged_cookies = logged_cookies
        response = await self.client.get(
            '/oauth/authorize?client_id=1&redirect_uri=https%3A%2F%2Fapp.hackthebox.com%2Fsso%2Flink&response_type=code&scope=',
            cookies=self.logged_cookies,
            follow_redirects=True
        )
        sso_code = str(response.url).split('=')
        await self.get_access_token_labs(sso_code[1])

    async def get_access_token_labs(self, sso_code: Optional[str]):
        """Retrieve the access token for the labs using the SSO code."""
        if sso_code:
            response = await self.client.get(f'{LABS_BASE}/api/v4/sso/callback?code={sso_code}')
            print(response.json())
        else:
            print("SSO code not found in the response URL")

    async def run(self):
        """Run the client to initialize, log in, and retrieve the access token for the labs."""
        await self.initialize()
        await self.do_login()
        await self.labs()

# for debugging
async def main():
    client = HTBClient('elliotandmrrobot@ro.ru', '')
    await client.run()

asyncio.run(main())
