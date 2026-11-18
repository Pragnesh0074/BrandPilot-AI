"""Pydantic schemas for the AI-Powered Website Link Analysis API."""

from typing import List, Optional
from pydantic import BaseModel, Field


class LinkAnalysisRequest(BaseModel):
    """Request payload for website analysis."""
    url: str = Field(..., description="Target website URL to analyze", example="https://example.com")


class BrandDetails(BaseModel):
    """Brand overview and category details."""
    name: str = Field(..., description="Identified brand name", example="ABC Technologies")
    category: str = Field(..., description="Main business category", example="Technology Services")
    summary: str = Field(..., description="Short business overview summary", example="A digital transformation firm.")


class CompetitorItem(BaseModel):
    """Details for a specific competitor."""
    brand_name: str = Field(..., description="Competitor brand name")
    main_service: str = Field(..., description="Primary service offered")
    target_market: str = Field(..., description="Competitor's target audience/market")
    strengths: str = Field(..., description="Competitor key strengths")
    weaknesses_or_gaps: str = Field(..., description="Competitor gaps or weaknesses")


class CompetitorAnalysis(BaseModel):
    """Section 1: Competitor vs Your Brand Details."""
    brand_overview: str = Field(..., description="Overview of the submitted brand")
    competitors: List[CompetitorItem] = Field(default_factory=list, description="Minimum 3 identified competitors")
    strengths: List[str] = Field(default_factory=list, description="Your brand's key strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Identified areas for brand growth")
    competitive_advantages: List[str] = Field(default_factory=list, description="Your unique advantages over competitors")
    opportunities: List[str] = Field(default_factory=list, description="Actionable market positioning opportunities")


class TargetSearchQuery(BaseModel):
    """Section 2: Top Target Search Query."""
    query: str = Field(..., description="High-intent search query phrase")
    platforms: List[str] = Field(..., description="Relevant platforms (Google, Facebook, Instagram, LinkedIn, X)")
    intent: str = Field(..., description="Search intent (e.g. Service Discovery, B2B Search, Inspiration)")
    business_relevance: str = Field(..., description="Why this query matters to the business")
    target_audience: str = Field(..., description="Target user group executing the query")


class SEOImprovements(BaseModel):
    """Section 3: SEO Improvement Recommendations."""
    primary_keyword: str = Field(..., description="Recommended primary keyword")
    secondary_keywords: List[str] = Field(default_factory=list, description="Recommended secondary keywords")
    long_tail_keywords: List[str] = Field(default_factory=list, description="High-intent long-tail keywords")
    business_keywords: List[str] = Field(default_factory=list, description="Industry/niche business keywords")
    recommended_title: str = Field(..., description="Optimized SEO Title (< 60 chars)")
    meta_description: str = Field(..., description="Compelling meta description (< 160 chars)")
    supporting_content: List[str] = Field(default_factory=list, description="Content ideas: landing pages, FAQs, blog topics")


class ServiceItem(BaseModel):
    """Section 4: Top Service Item."""
    service_name: str = Field(..., description="Name of the service")
    description: str = Field(..., description="Short explanation of the service")
    target_industry: str = Field(..., description="Relevant industry sector")
    target_customer: str = Field(..., description="Potential customer type or persona")
    main_benefit: str = Field(..., description="Primary customer value proposition")


class TargetAudience(BaseModel):
    """Section 5: Target Audience Identification."""
    primary_audience: List[str] = Field(default_factory=list, description="Primary customer segments")
    secondary_audience: List[str] = Field(default_factory=list, description="Secondary customer segments")
    industries: List[str] = Field(default_factory=list, description="Relevant industry sectors")
    business_types: List[str] = Field(default_factory=list, description="Types of businesses targeted (e.g. SMBs, Enterprises)")
    customer_profiles: List[str] = Field(default_factory=list, description="Key persona profiles")
    location: Optional[str] = Field(None, description="Geographic or market focus")
    customer_needs: List[str] = Field(default_factory=list, description="Core customer pain points and needs")
    potential_interests: List[str] = Field(default_factory=list, description="Customer professional or personal interests")
    recommended_segments: List[str] = Field(default_factory=list, description="Recommended marketing target segments")


class AnalysisContent(BaseModel):
    """Complete 5-section analysis container."""
    competitor_analysis: CompetitorAnalysis
    target_search_queries: List[TargetSearchQuery]
    seo_improvements: SEOImprovements
    top_services: List[ServiceItem]
    target_audience: TargetAudience


class LinkAnalysisResponse(BaseModel):
    """Final JSON response for the Link Analysis API."""
    success: bool = True
    website: str
    brand: BrandDetails
    analysis: AnalysisContent
    model_used: Optional[str] = None
    processing_time_ms: Optional[float] = None
