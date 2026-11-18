"""Pydantic schemas package."""

from app.schemas.link_analysis import (
    LinkAnalysisRequest,
    LinkAnalysisResponse,
    BrandDetails,
    CompetitorAnalysis,
    TargetSearchQuery,
    SEOImprovements,
    ServiceItem,
    TargetAudience,
    AnalysisContent,
)
from app.schemas.posting import (
    PostingRequest,
    PostingResponse,
    PlatformPostResult,
)

__all__ = [
    "LinkAnalysisRequest",
    "LinkAnalysisResponse",
    "BrandDetails",
    "CompetitorAnalysis",
    "TargetSearchQuery",
    "SEOImprovements",
    "ServiceItem",
    "TargetAudience",
    "AnalysisContent",
    "PostingRequest",
    "PostingResponse",
    "PlatformPostResult",
]
