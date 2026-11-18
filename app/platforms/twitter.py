"""X / Twitter API v2 integration."""

import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas.posting import PlatformPostResult


class TwitterPlatform(BasePlatform):
    """Publishes public posts (tweets) via Twitter API v2."""

    def __init__(self):
        super().__init__(name="X (Twitter)", is_public=True)
        self.bearer_token = settings.TWITTER_BEARER_TOKEN

    async def post(self, message: str, cta_url: str) -> PlatformPostResult:
        if not self.bearer_token:
            if settings.POSTING_SIMULATION_MODE:
                return self.create_success_result(
                    posted_url="https://x.com/BrandHandle/status/179283749281736452"
                )
            return self.create_failed_result("Missing TWITTER_BEARER_TOKEN.")

        api_url = "https://api.twitter.com/2/tweets"
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
        }
        payload = {"text": message}

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(api_url, headers=headers, json=payload)
                if res.is_success:
                    data = res.json()
                    tweet_id = data.get("data", {}).get("id")
                    return self.create_success_result(
                        posted_url=f"https://x.com/i/web/status/{tweet_id}"
                    )
                return self.create_failed_result(f"Twitter API error {res.status_code}: {res.text}")
        except Exception as e:
            return self.create_failed_result(f"Network error connecting to Twitter: {str(e)}")
