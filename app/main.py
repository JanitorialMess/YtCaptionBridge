from email.policy import default
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router
from .core.logging import setup_logging
from .config import get_settings
from slowapi import Limiter
from slowapi.middleware import SlowAPIASGIMiddleware  # Changed this line
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

setup_logging()
settings = get_settings()

app = FastAPI(
    title=settings.project_name,
    openapi_url=f"{settings.api_base}/openapi.json",
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.rate_limit_enabled:
    @app.exception_handler(RateLimitExceeded)
    async def custom_rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={
                "error_code": "RATE_LIMIT_EXCEEDED",
                "error_message": f"Rate limit exceeded: {settings.rate_limit}"
            }
        )
    app.state.limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])
    app.add_middleware(SlowAPIASGIMiddleware)

app.include_router(router, prefix=settings.api_base)
