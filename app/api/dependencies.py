from ..services.transcript_service import TranscriptService

async def get_transcript_service() -> TranscriptService:
    return TranscriptService() 