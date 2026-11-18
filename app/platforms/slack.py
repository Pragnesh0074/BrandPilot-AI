"""Slack Incoming Webhook integration (100% Free)."""

import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas.posting import PlatformPostResult


class SlackPlatform(BasePlatform):
    """Publishes messages to Slack workspaces via Incoming Webhooks."""

    def __init__(self):
        super().__init__(name="Slack", is_public=False)
        self.webhook_url = settings.SLACK_WEBHOOK_URL

    async def post(self, message: str, cta_url: str) -> PlatformPostResult:
        if not self.webhook_url:
            if settings.POSTING_SIMULATION_MODE:
                return self.create_success_result(
                    posted_url="https://app.slack.com/client/T00000000/C00000000"
                )
            return self.create_failed_result("Missing SLACK_WEBHOOK_URL.")

        payload = {"text": message}

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(self.webhook_url, json=payload)
                if res.is_success and res.text.strip().lower() == "ok":
                    return self.create_success_result(
                        posted_url="https://app.slack.com/client"
                    )
                return self.create_failed_result(f"Slack returned status {res.status_code}: {res.text}")
        except Exception as e:
            return self.create_failed_result(f"Network error connecting to Slack: {str(e)}")
