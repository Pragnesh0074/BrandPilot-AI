"""FastAPI router for Automated Multi-Platform Posting."""

from fastapi import APIRouter, HTTPException, status
from app.schemas.posting import PostingRequest, PostingResponse
from app.services.posting_service import PostingService

router = APIRouter(tags=["Multi-Platform Posting"])
posting_service = PostingService()


@router.post(
    "/posting",
    response_model=PostingResponse,
    status_code=status.HTTP_200_OK,
    summary="Publish short message across 5+ platforms",
    description=(
        "Automatically validates and publishes a message with exactly one CTA link "
        "across at least 5 third-party platforms (Telegram, Discord, Slack, Mastodon, Bluesky). "
        "Fault-isolated design ensures independent execution per platform."
    ),
)
async def post_message(request: PostingRequest):
    """
    Endpoint for automated multi-platform distribution:
    - Input: Short message (<=200 chars) with exactly 1 CTA link
    - Output: Individual platform publishing statuses and public URLs
    """
    try:
        response = await posting_service.publish_message(request.message)
        return response
    except ValueError as e:
        # Input validation violation (length > 200, 0 links, >1 links, invalid URL)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while dispatching posts: {str(e)}",
        )
