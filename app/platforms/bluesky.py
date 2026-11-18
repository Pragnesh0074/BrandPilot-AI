"""Bluesky Social AT Protocol API (100% Free & Open Social Network)."""

from datetime import datetime, timezone
import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas.posting import PlatformPostResult


class BlueskyPlatform(BasePlatform):
    """Publishes public posts to Bluesky via AT Protocol."""

    def __init__(self):
        super().__init__(name="Bluesky", is_public=True)
        self.handle = settings.BLUESKY_HANDLE
        self.app_password = settings.BLUESKY_APP_PASSWORD

    async def post(self, message: str, cta_url: str) -> PlatformPostResult:
        if not self.handle or not self.app_password:
            if settings.POSTING_SIMULATION_MODE:
                clean_handle = self.handle or "brand.bsky.social"
                return self.create_success_result(
                    posted_url=f"https://bsky.app/profile/{clean_handle}/post/3kmv4q2xyz"
                )
            return self.create_failed_result("Missing BLUESKY_HANDLE or BLUESKY_APP_PASSWORD.")

        auth_url = "https://bsky.social/xrpc/com.atproto.server.createSession"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # 1. Create Session
                auth_res = await client.post(
                    auth_url,
                    json={"identifier": self.handle, "password": self.app_password},
                )
                if not auth_res.is_success:
                    return self.create_failed_result(f"Bluesky auth failed: {auth_res.text}")

                auth_data = auth_res.json()
                access_jwt = auth_data["accessJwt"]
                did = auth_data["did"]

                # 2. Create Record (Post)
                create_record_url = "https://bsky.social/xrpc/com.atproto.repo.createRecord"
                headers = {"Authorization": f"Bearer {access_jwt}"}
                now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

                record_payload = {
                    "repo": did,
                    "collection": "app.bsky.feed.post",
                    "record": {
                        "$type": "app.bsky.feed.post",
                        "text": message,
                        "createdAt": now_iso,
                    },
                }

                post_res = await client.post(create_record_url, headers=headers, json=record_payload)
                if post_res.is_success:
                    post_data = post_res.json()
                    rkey = post_data["uri"].split("/")[-1]
                    return self.create_success_result(
                        posted_url=f"https://bsky.app/profile/{self.handle}/post/{rkey}"
                    )
                return self.create_failed_result(f"Bluesky post creation failed: {post_res.text}")
        except Exception as e:
            return self.create_failed_result(f"Network error connecting to Bluesky: {str(e)}")
