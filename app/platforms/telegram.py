"""Telegram Bot API integration (100% Free)."""

import httpx
from app.config import Settings
from app.platforms.base import BasePlatform
from app.schemas.posting import PlatformPostResult


class TelegramPlatform(BasePlatform):
    """Publishes messages to public Telegram channels or groups via Telegram Bot API."""

    def __init__(self):
        super().__init__(name="Telegram", is_public=True)

    @property
    def bot_token(self):
        return Settings().TELEGRAM_BOT_TOKEN

    @property
    def chat_id(self):
        return Settings().TELEGRAM_CHAT_ID

    async def post(self, message: str, cta_url: str) -> PlatformPostResult:
        bot_token = self.bot_token
        chat_id = self.chat_id

        if not bot_token or not chat_id:
            if Settings().POSTING_SIMULATION_MODE:
                clean_chat = (chat_id or "channel").replace("@", "")
                return self.create_success_result(
                    posted_url=f"https://t.me/{clean_chat}/1042"
                )
            return self.create_failed_result("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID.")

        api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "disable_web_page_preview": False,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(api_url, json=payload)
                data = res.json()
                if res.is_success and data.get("ok"):
                    msg_id = data["result"]["message_id"]
                    clean_chat = str(chat_id).replace("@", "")
                    return self.create_success_result(
                        posted_url=f"https://t.me/{clean_chat}/{msg_id}"
                    )
                return self.create_failed_result(
                    data.get("description", f"Telegram API error {res.status_code}")
                )
        except Exception as e:
            return self.create_failed_result(f"Network error connecting to Telegram: {str(e)}")
