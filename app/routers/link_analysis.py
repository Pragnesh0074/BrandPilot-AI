"""FastAPI router for AI-Powered Website Link Analysis."""

from fastapi import APIRouter, HTTPException, status
from app.schemas.link_analysis import LinkAnalysisRequest, LinkAnalysisResponse
from app.services.analysis_service import AnalysisService

router = APIRouter(tags=["AI Link Analysis"])
analysis_service = AnalysisService()


@router.post(
    "/link-analysis",
    response_model=LinkAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze website link using Free AI",
    description=(
        "Analyzes a submitted website URL using an intelligent, free AI engine. "
        "Extracts brand information, generates competitor benchmarking, target search queries, "
        "actionable SEO recommendations, top 5 services, and target audience segments. "
        "Includes built-in SSRF protection against private networks."
    ),
)
async def analyze_link(request: LinkAnalysisRequest):
    """
    Endpoint for website link intelligence:
    - Input: JSON containing target website URL
    - Output: 5 structured analysis sections with zero paid API requirement
    """
    try:
        response = await analysis_service.analyze(request.url)
        return response
    except ValueError as e:
        # Client input validation error or SSRF security block
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        # Unexpected processing error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while analyzing the website: {str(e)}",
        )
