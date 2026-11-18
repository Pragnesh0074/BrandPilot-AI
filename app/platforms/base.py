"""Abstract base class for third-party publishing platforms."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from app.schemas.posting import PlatformPostResult


class BasePlatform(ABC):
    """Base class for all multi-platform posting integrations."""

    def __init__(self, name: str, is_public: bool = True):
        self.name = name
        self.is_public = is_public

    @abstractmethod
    async def post(self, message: str, cta_url: str) -> PlatformPostResult:
        """
        Publish message to the platform.
        Must return PlatformPostResult and never raise unhandled exceptions.
        """
        pass

    def get_current_date_time(self):
        """Helper to get current ISO date and time."""
        now = datetime.now()
        return now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")

    def create_success_result(self, posted_url: str) -> PlatformPostResult:
        """Create standard success result."""
        date_str, time_str = self.get_current_date_time()
        return PlatformPostResult(
            platform=self.name,
            status="success",
            posted_url=posted_url,
            public_access=self.is_public,
            date=date_str,
            time=time_str,
            error=None,
        )

    def create_failed_result(self, error_message: str) -> PlatformPostResult:
        """Create standard failure result."""
        return PlatformPostResult(
            platform=self.name,
            status="failed",
            posted_url=None,
            public_access=self.is_public,
            date=None,
            time=None,
            error=error_message,
        )
