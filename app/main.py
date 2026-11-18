"""Main FastAPI Application Entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import link_analysis_router, posting_router

app = FastAPI(
    title="AI Link Analysis & Multi-Platform Posting API",
    description=(
        "Production-grade FastAPI practical test implementation featuring:\n"
        "1. **AI-Powered Website Link Analysis** (`POST /link-analysis`) with 100% Free AI intelligence.\n"
        "2. **Automated Multi-Platform Posting** (`POST /posting`) supporting 5+ platforms with fault isolation.\n"
        "3. Built-in SSRF protection, strict input validation, and zero mandatory paid credentials."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Core API Routers
app.include_router(link_analysis_router)
app.include_router(posting_router)


@app.get("/", tags=["System"])
async def root():
    """Root status endpoint with service discovery metadata."""
    return {
        "status": "online",
        "service": "AI Link Analysis & Multi-Platform Posting API",
        "documentation": "/docs",
        "endpoints": {
            "link_analysis": "POST /link-analysis",
            "multi_platform_posting": "POST /posting",
            "health": "GET /health",
        },
        "llm_engine": {
            "mode": "100% Free AI",
            "active_provider": settings.LLM_PROVIDER,
            "cost_per_request": "$0.00",
        },
    }


@app.get("/health", tags=["System"])
async def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "free_ai_ready": True,
        "posting_simulation_mode": settings.POSTING_SIMULATION_MODE,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
