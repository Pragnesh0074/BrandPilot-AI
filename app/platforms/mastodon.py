"""Mastodon Decentralized Social Network REST API (100% Free & Open Source)."""

import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas.posting import PlatformPostResult


class MastodonPlatform(BasePlatform):
    """Publishes public toots to the Mastodon decentralized social network."""

    def __init__(self):
        super().__init__(name="Mastodon", is_public=True)
        self.instance_url = settings.MASTODON_INSTANCE_URL.rstrip("/")
        self.access_token = settings.MASTODON_ACCESS_TOKEN

    async def post(self, message: str, cta_url: str) -> PlatformPostResult:
        if not self.access_token:
            if settings.POSTING_SIMULATION_MODE:
                return self.create_success_result(
                    posted_url=f"{self.instance_url}/@brand/1124589201948301"
                )
            return self.create_failed_result("Missing MASTODON_ACCESS_TOKEN.")

        api_url = f"{self.instance_url}/api/v1/statuses"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        payload = {
            "status": message,
            "visibility": "public",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(api_url, headers=headers, json=payload)
                if res.is_success:
                    data = res.json()
                    post_url = data.get("url") or f"{self.instance_url}/statuses/{data.get('id')}"
                    return self.create_success_result(posted_url=post_url)
                return self.create_failed_result(f"Mastodon returned status {res.status_code}: {res.text}")
        except Exception as e:
            return self.create_failed_result(f"Network error connecting to Mastodon: {str(e)}")
