from youtube_transcript_api import (
    YouTubeTranscriptApi,
    NoTranscriptFound,
    VideoUnavailable,
    TranscriptsDisabled,
)
from youtube_transcript_api.formatters import (
    JSONFormatter,
    TextFormatter,
    WebVTTFormatter,
    SRTFormatter,
)
from ..schemas.transcript import (
    CaptionsType,
    TranscriptResponse,
    OutputFormat,
)
from ..exceptions.transcript_exceptions import (
    VideoNotFoundException,
    LanguageNotAvailableException,
    TranscriptServiceException,
)

import json
from typing import Optional
from loguru import logger
from fastapi import status, HTTPException

class TranscriptService:
    @staticmethod
    async def get_transcript(
        video_id: str,
        language: str,
        auto: bool = False,
        translate: Optional[str] = None,
        prefer: Optional[CaptionsType] = CaptionsType.MANUAL,
        output_format: OutputFormat = OutputFormat.JSON,
    ) -> TranscriptResponse:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            was_translated = False
            available_translations = []
            
            try:
                if auto and prefer == CaptionsType.AUTO:
                    transcript = transcript_list.find_generated_transcript([language])
                elif auto:
                    # Give priority to manual transcripts since they tend to be more accurate
                    transcript = transcript_list.find_transcript([language])
                else:
                    transcript = transcript_list.find_manually_created_transcript([language])
                
                # Get available translations for the found transcript
                if hasattr(transcript, 'translation_languages'):
                    available_translations = [
                        lang['language_code'] 
                        for lang in transcript.translation_languages
                    ]
                
                if translate and translate != language:
                    if not transcript.is_translatable:
                        raise TranscriptServiceException(
                            f"Translation is not available from {language} for this video",
                            error_code="TRANSLATION_NOT_AVAILABLE",
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
                        )
                    
                    if translate not in available_translations:
                        raise LanguageNotAvailableException(
                            translate,
                            video_id,
                            available_translations
                        )
                    
                    transcript = transcript.translate(translate)
                    was_translated = True
                    
            except NoTranscriptFound:
                # Get list of available languages based on auto parameter
                available_languages = (
                    [t.language_code for t in transcript_list._generated_transcripts.values()]
                    if auto else
                    [t.language_code for t in transcript_list._manually_created_transcripts.values()]
                )
                
                raise LanguageNotAvailableException(
                    language,
                    video_id,
                    available_languages
                )
            
            data = transcript.fetch()
            
            formatter = {
                OutputFormat.JSON: JSONFormatter(),
                OutputFormat.TEXT: TextFormatter(),
                OutputFormat.SRT: SRTFormatter(),
                OutputFormat.VTT: WebVTTFormatter(),
            }.get(output_format)
            
            if not formatter:
                raise TranscriptServiceException(
                    message="Unsupported output format",
                    error_code="INVALID_FORMAT",
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            
            if output_format == OutputFormat.JSON:
                formatted_transcript = json.loads(formatter.format_transcript(data))
            else:
                formatted_transcript = formatter.format_transcript(data)
            
            response = TranscriptResponse(
                video_id=video_id,
                language=translate if was_translated else language,
                auto_generated=auto,
                was_translated=was_translated,
                transcript=formatted_transcript,
                available_languages=available_translations,
            )
            return response
                
        except VideoUnavailable:
            raise VideoNotFoundException(video_id)
        except TranscriptsDisabled:
            raise TranscriptServiceException(
                message="Transcripts are disabled for this video",
                error_code="TRANSCRIPTS_DISABLED",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            error_msg = str(e)
            if "422" in error_msg and "LANGUAGE_NOT_AVAILABLE" in error_msg:
                raise LanguageNotAvailableException(language, video_id)
            
            logger.error(f"Transcript service error: {error_msg}")
            raise TranscriptServiceException(
                message="Failed to fetch transcript",
                error_code="TRANSCRIPT_SERVICE_ERROR",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )