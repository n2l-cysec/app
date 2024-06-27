from typing import Optional, Tuple
import httpx
from .const import API_BASE
from .labs import HTBLabs
            
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
        self.client = httpx.AsyncClient(base_url=api_base, headers={'Accept': 'application/json'}, timeout=60)
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
    
    async def do_login(self) -> Tuple[httpx.Cookies, str]:
        """
        Authenticate the user using the provided email and password.
        
        Returns:
            httpx.Cookies: a logged cookies.
            sso_code: a sso_code to get the access_token for labs,academy and many more.
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
        sso_code = await self.sso()
        return self.logged_cookies, sso_code
    
    async def sso(
        self,
        logged_cookies: Optional[str] = None
    ) -> str : 
        """
        Initiate the SSO process and retrieve the SSO code from logged_cookies.

        Args:
            logged_cookies (Optional[httpx.Cookies]): The cookies to use for the request. If None, uses the client's logged cookies.
        """
        if logged_cookies:
            self.logged_cookies = logged_cookies
        response = await self.client.get(
            '/oauth/authorize?client_id=1&redirect_uri=https%3A%2F%2Fapp.hackthebox.com%2Fsso%2Flink&response_type=code&scope=',
            cookies=self.logged_cookies,
            follow_redirects=True
        )
        return str(response.url).split('=')[1]
    

    async def run(self) -> str:
        """Run the client to initialize, log in, and retrieve the access token for the labs."""
        await self.initialize()
        _, sso_code = await self.do_login()
        return sso_code
        # HTBLabs(sso_code=sso_code).get_user_progress()


