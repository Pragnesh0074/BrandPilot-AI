"""Pydantic schemas for Automated Multi-Platform Posting API."""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class PostingRequest(BaseModel):
    """Request schema for posting across multiple platforms."""
    message: str = Field(
        ...,
        description="Message content with exactly one CTA link, maximum 200 characters.",
        example="Check out our latest business platform and grow your online visibility. https://example.com"
    )


class PlatformPostResult(BaseModel):
    """Result details of a post attempt on a specific platform."""
    platform: str = Field(..., description="Name of the platform")
    status: Literal["success", "failed"] = Field(..., description="Posting status: success or failed")
    posted_url: Optional[str] = Field(None, description="Publicly accessible URL of the published post")
    public_access: bool = Field(..., description="Whether the posted content is publicly accessible")
    date: Optional[str] = Field(None, description="Date of posting (YYYY-MM-DD)")
    time: Optional[str] = Field(None, description="Time of posting (HH:MM:SS)")
    error: Optional[str] = Field(None, description="Error message if posting failed")


class PostingResponse(BaseModel):
    """Response returned by POST /posting."""
    success: bool = Field(..., description="Overall request execution status")
    results: List[PlatformPostResult] = Field(..., description="Posting outcome across each integrated platform")
