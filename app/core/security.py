from fastapi import Security, HTTPException
from fastapi.security import APIKeyQuery
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from ..config import get_settings

settings = get_settings()

api_key_header = APIKeyQuery(name=settings.api_key_name, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if not api_key_header or api_key_header != settings.api_key:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API key"
        )
    return api_key_header
