from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union
from enum import Enum

class OutputFormat(str, Enum):
    JSON = "json"
    TEXT = "txt"
    SRT = "srt"
    VTT = "vtt"

class TranscriptRequest(BaseModel):
    video_id: str
    language: str
    auto: bool = False
    target_language: Optional[str] = None
    output_format: OutputFormat = OutputFormat.JSON

class TranscriptResponse(BaseModel):
    video_id: str
    language: str
    auto_generated: bool
    was_translated: bool
    available_translations: Optional[List[str]] = None
    formatted_content: Any
class ErrorResponse(BaseModel):
    error: str
    message: str
    available_languages: Optional[List[str]] = None
    available_translations: Optional[List[str]] = None
