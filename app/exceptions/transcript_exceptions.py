from fastapi import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_400_BAD_REQUEST,
)

class VideoNotFoundException(HTTPException):
    def __init__(self, video_id: str):
        super().__init__(
            status_code=HTTP_404_NOT_FOUND,
            detail={
                "error_code": "VIDEO_NOT_FOUND",
                "error_message": f"Video {video_id} was not found"
            }
        )

class LanguageNotAvailableException(HTTPException):
    def __init__(self, language: str, video_id: str, available_languages: list = None):
        detail = {
            "error_code": "LANGUAGE_NOT_AVAILABLE",
            "error_message": f"Language {language} is not available for video {video_id}"
        }
        if available_languages:
            detail["available_languages"] = available_languages
        
        super().__init__(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

class NoManualTranscriptException(HTTPException):
    def __init__(self, language: str, video_id: str):
        super().__init__(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error_code": "NO_MANUAL_TRANSCRIPT",
                "error_message": f"No manual transcript available in {language} for video {video_id}"
            }
        )

class TranscriptServiceException(HTTPException):
    def __init__(self, message: str, error_code: str = "TRANSCRIPT_SERVICE_ERROR", status_code: int = HTTP_400_BAD_REQUEST):
        super().__init__(
            status_code=status_code,
            detail={
                "error_code": error_code,
                "error_message": message
            }
        )