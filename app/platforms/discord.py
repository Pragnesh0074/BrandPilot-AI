"""Discord Webhook integration (100% Free)."""

import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas.posting import PlatformPostResult


class DiscordPlatform(BasePlatform):
    """Publishes messages to Discord channels via Discord Webhook API."""

    def __init__(self):
        super().__init__(name="Discord", is_public=True)
        self.webhook_url = settings.DISCORD_WEBHOOK_URL

    async def post(self, message: str, cta_url: str) -> PlatformPostResult:
        if not self.webhook_url:
            if settings.POSTING_SIMULATION_MODE:
                return self.create_success_result(
                    posted_url="https://discord.com/channels/123456789012345678/987654321098765432/1122334455"
                )
            return self.create_failed_result("Missing DISCORD_WEBHOOK_URL.")

        payload = {"content": message}
        # ?wait=true returns the created message object containing the message ID
        target_url = f"{self.webhook_url}?wait=true"

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(target_url, json=payload)
                if res.is_success:
                    data = res.json()
                    channel_id = data.get("channel_id", "channel")
                    msg_id = data.get("id", "msg")
                    return self.create_success_result(
                        posted_url=f"https://discord.com/channels/@me/{channel_id}/{msg_id}"
                    )
                return self.create_failed_result(f"Discord returned status {res.status_code}: {res.text}")
        except Exception as e:
            return self.create_failed_result(f"Network error connecting to Discord: {str(e)}")
