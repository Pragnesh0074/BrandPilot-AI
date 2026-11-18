"""Orchestrates link extraction, SSRF security validation, and AI business analysis."""

import time
from app.schemas.link_analysis import LinkAnalysisResponse
from app.services.website_extractor import WebsiteExtractor
from app.services.llm_service import LLMService
from app.utils.validators import validate_and_sanitize_url


class AnalysisService:
    """Service orchestrating website scraping and LLM analysis."""

    def __init__(self):
        self.extractor = WebsiteExtractor()
        self.llm_service = LLMService()

    async def analyze(self, raw_url: str) -> LinkAnalysisResponse:
        """
        Validate URL, fetch web content, invoke Free AI engine, and return structured analysis.
        """
        start_time = time.perf_counter()

        # Step 1: Validate URL and enforce SSRF protection
        sanitized_url = validate_and_sanitize_url(raw_url)

        # Step 2: Fetch and extract HTML content
        extracted_data = await self.extractor.extract(sanitized_url)

        # Step 3: Run AI / LLM analysis
        analysis_result = await self.llm_service.analyze_website(extracted_data)

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # Step 4: Return formatted structured response
        return LinkAnalysisResponse(
            success=True,
            website=sanitized_url,
            brand=analysis_result["brand"],
            analysis=analysis_result["analysis"],
            model_used=analysis_result.get("model_used"),
            processing_time_ms=elapsed_ms,
        )
