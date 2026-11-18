"""Orchestrates concurrent multi-platform posting with fault isolation."""

import asyncio
from typing import List
from app.platforms import (
    BasePlatform,
    TelegramPlatform,
    DiscordPlatform,
    SlackPlatform,
    MastodonPlatform,
    BlueskyPlatform,
)
from app.schemas.posting import PlatformPostResult, PostingResponse
from app.utils.validators import validate_posting_message


class PostingService:
    """Service that manages independent concurrent postings to third-party platforms."""

    def __init__(self, platforms: List[BasePlatform] = None):
        self.platforms = platforms or [
            TelegramPlatform(),
            DiscordPlatform(),
            SlackPlatform(),
            MastodonPlatform(),
            BlueskyPlatform(),
        ]

    async def _safe_post(self, platform: BasePlatform, message: str, cta_url: str) -> PlatformPostResult:
        """Execute a single platform post with guaranteed exception safety."""
        try:
            return await platform.post(message, cta_url)
        except Exception as e:
            return platform.create_failed_result(f"Unexpected error: {str(e)}")

    async def publish_message(self, raw_message: str) -> PostingResponse:
        """
        Validate input constraints and dispatch message concurrently to all platforms.
        Independent error handling ensures a failure in one platform never blocks others.
        """
        # Validate constraints: length <= 200 and exactly one valid CTA link
        sanitized_message, cta_url = validate_posting_message(raw_message)

        # Dispatch concurrently to all configured platforms
        tasks = [
            self._safe_post(platform, sanitized_message, cta_url)
            for platform in self.platforms
        ]
        results = await asyncio.gather(*tasks)

        return PostingResponse(
            success=True,
            results=list(results),
        )
