from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union
from enum import Enum

class OutputFormat(str, Enum):
    JSON = "json"
    TEXT = "txt"
    SRT = "srt"
    VTT = "vtt"
    
class CaptionsType(str, Enum):
    AUTO = "auto"
    MANUAL = "manual"

class TranscriptRequest(BaseModel):
    video_id: str
    language: str
    auto: bool = False
    translate: Optional[str] = None
    prefer: Optional[CaptionsType] = CaptionsType.MANUAL
    output_format: OutputFormat = OutputFormat.JSON

class TranscriptResponse(BaseModel):
    video_id: str
    language: str
    auto_generated: bool
    was_translated: bool
    available_translations: Optional[List[str]] = None
    transcript: Any
class ErrorResponse(BaseModel):
    error: str
    message: str
    available_languages: Optional[List[str]] = None
    available_translations: Optional[List[str]] = None
