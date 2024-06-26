
from typing import Optional
import httpx

API_BASE = "https://account.hackthebox.com"

class HTBClient:
    def __init__(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        api_base: str = API_BASE,
    ):
        self.c = httpx.Client(base_url=api_base, headers={
            'Accept':'application/json'
        })
        self._api_base = api_base
        self.initialize()
        self.do_login(email, password)

    def initialize(self):
        r = self.c.get('/api/v1/csrf-cookie')
        self.cookies = r.cookies
        self.csrftoken = r.cookies["XSRF-TOKEN"].replace("%3D", "=")
        
    def do_login(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ):
        
        r = self.c.post('/api/v1/auth/login',json={
            "email":email,
            "password":password,
            "remember":True,
        }, headers={
            "X-Xsrf-Token":self.csrftoken
        }, cookies=self.cookies).json()
        print(r)
        
# for debugging
HTBClient('elliotandmrrobot@ro.ru','')