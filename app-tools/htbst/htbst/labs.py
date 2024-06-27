from typing import Optional
import httpx
from .const import LABS_BASE

class HTBLabs:
    def __init__(
        self,
        sso_code: str,
        access_token: Optional[str] = None,
    ):
        """
        Initialize the HTBLabs client with an SSO code and optionally an access token.

        Args:
            sso_code (str): The SSO code obtained during authentication.
            access_token (Optional[str]): An optional access token. If not provided, it will be retrieved using the SSO code.
        """
        self.client = httpx.Client(base_url=LABS_BASE, headers={
            'Accept': 'application/json',
        },timeout=60)
        if not access_token:
            self.access_token = self.get_access_token_labs(sso_code)
        else:
            self.access_token = access_token
        self.client.headers.update({'Authorization': f'Bearer {self.access_token}'})

    def get_access_token_labs(
        self, 
        sso_code: Optional[str] = None
    ) -> str:
        """
        Retrieve the access token for the labs using the SSO code.
        
        Args:
            sso_code (Optional[str]): The SSO code obtained during authentication.
            
        Returns:
            str: A bearer access token to access labs.
            
        Example:
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ..."
        """
        if sso_code:
            response = self.client.get(f'/api/v4/sso/callback?code={sso_code}')
            self.access_token = response.json()["message"]["access_token"]
            return self.access_token
        else:
            raise ValueError("SSO code not found in the response URL")

    def get_user_progress(self) -> dict:
        """
        Retrieve the user's progress in the labs.

        Returns:
            dict: A dictionary containing the user's progress data.
            
        Example:
            {
                "data": {
                    "sps": [
                        {
                            "id": 1,
                            "name": "Tier 0",
                            "completion_percentage": 39,
                            "free_machine_completion_percentage": 72,
                            "avatar": "https://labs.hackthebox.com/storage/starting-points/tiers/abaa159b15e1bcde9045ba65f73eb5be.png"
                        }
                    ],
                    "machines": [
                        {
                            "id": 484,
                            "name": "Support",
                            "os": "Windows",
                            "points": 0,
                            "difficulty": "Easy",
                            "avatar": "/storage/avatars/833a3b1f7f96b5708d19b6de084c3201.png",
                            "user_flag": 1,
                            "root_flag": 0,
                            "url": "/machines/Support"
                        }
                        ...
                    ],
                    "tracks": [
                        {
                            "id": 21,
                            "name": "Intro to Reversing",
                            "difficulty": "Easy",
                            "points": 190,
                            "percentage": 30,
                            "avatar": "/storage/tracks/21.png",
                            "url": "/tracks/Intro-to-Reversing"
                        }
                    ],
                    "fortresses": [],
                    "endgames": [],
                    "prolabs": []
                }
            }
        """
        response = self.client.get('/api/v4/home/user/progress')
        return response.json()

    def get_user_summary(self) -> dict:
        """
        Retrieve a summary of the user's profile.

        Returns:
            dict: A dictionary containing the user's profile summary.
            
        Example:
            {
                "userStats": {
                    "id": 1924182,
                    "sso_id": 1916697,
                    "name": "projectelliot",
                    "system_owns": 11,
                    "user_owns": 16,
                    "user_bloods": 0,
                    "system_bloods": 0,
                    "team": null,
                    "respects": 0,
                    "rank": "Hacker",
                    "rank_id": 3,
                    "current_rank_progress": 67.52,
                    "next_rank": "Pro Hacker",
                    "next_rank_points": 16.596,
                    "rank_ownership": 36.88,
                    "rank_requirement": 20,
                    "ranking": 716,
                    "subscription": "VIP+",
                    "points": 168,
                    "growths": {
                        "rank": 716,
                        "previous_rank": 871,
                        "rank_growth": "17.80",
                        "points": 168,
                        "previous_points": 0,
                        "points_growth": "100.00",
                        "compared_to_date": "2024-04-16T22:03:49.000000Z"
                    },
                    "rankingGraphStats": {
                        "points_diff": 168,
                        "points_growth": "100.00",
                        "ranks_diff": 155,
                        "chart_data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 39, 168]
                    }
                }
            }
        """
        response = self.client.get('/api/v4/user/profile/summary')
        return response.json()

    def get_user_rank(self) -> dict:
        """
        Retrieve the user's rank information.

        Returns:
            dict: A dictionary containing the user's rank information.
            
        Example:
            {
                "data": {
                    "sso_linked": true,
                    "ranking": {
                        "name": "Hacker",
                        "id": 3,
                        "current_xp": 36.88,
                        "next_rank_xp": 45
                    },
                    "season_ranking": {
                        "league": "Ruby",
                        "rank": 887,
                        "rank_suffix": "th",
                        "latest_season": {
                            "id": 5,
                            "name": "Season 5"
                        },
                        "upcoming_season": {
                            "id": null,
                            "name": null,
                            "date": null
                        }
                    }
                }
            }
        """
        response = self.client.get('/api/v4/navigation/main')
        return response.json()
