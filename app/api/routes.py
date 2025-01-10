from fastapi import APIRouter, Depends, Query
from ..schemas.transcript import TranscriptResponse, OutputFormat
from ..services.transcript_service import TranscriptService
from ..core.security import get_api_key
from .dependencies import get_transcript_service
from typing import Optional
from ..config import get_settings

settings = get_settings()
router = APIRouter()

@router.get(
    "/transcripts/{video_id}/lang/{language}.{format}",
    response_model=TranscriptResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(get_api_key)]
)
async def get_transcript(
    video_id: str,
    language: str,
    format: OutputFormat,
    auto: bool = Query(False, description="Whether to use auto-generated subtitles"),
    target_language: Optional[str] = Query(None, description="Specific language to translate to"),
    transcript_service: TranscriptService = Depends(get_transcript_service),
) -> TranscriptResponse:
    return await transcript_service.get_transcript(
        video_id=video_id,
        language=language,
        auto=auto,
        target_language=target_language,
        output_format=format,
    )