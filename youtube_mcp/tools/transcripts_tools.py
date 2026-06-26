"""Transcripts group: get_video_transcript, list_video_transcripts."""

import logging
from typing import Optional

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

from ..logging_utils import ToolLogger
from ..schemas import (
    GetVideoTranscriptResult,
    ListVideoTranscriptsResult,
    TranscriptData,
    TranscriptListData,
    TranscriptSegment,
    TranscriptTrack,
    ToolError,
)

logger = logging.getLogger("youtube-mcp.tools.transcripts")


def register_transcripts_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_video_transcript",
        description=(
            "Fetch the transcript (captions) for a YouTube video as plain text and "
            "individual timed segments. Uses auto-generated or manually created captions. "
            "Specify preferred languages in priority order; falls back to the first available "
            "if none match."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_video_transcript(
        video_id: str = Field(..., description="YouTube video ID. Required."),
        languages: Optional[list[str]] = Field(
            default=None,
            description=(
                "Preferred language codes in priority order (e.g. ['en', 'fr']). "
                "Omit to use the video's default language."
            ),
        ),
    ) -> GetVideoTranscriptResult:
        tlog = ToolLogger(logger, "get_video_transcript")
        try:
            kwargs = {"languages": languages} if languages else {}
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            if languages:
                try:
                    transcript = transcript_list.find_transcript(languages)
                except NoTranscriptFound:
                    transcript = transcript_list.find_generated_transcript(languages)
            else:
                transcript = next(iter(transcript_list))

            raw = transcript.fetch()
            segments = [
                TranscriptSegment(text=s["text"], start=s["start"], duration=s["duration"])
                for s in raw
            ]
            full_text = " ".join(s["text"] for s in raw)
            data = TranscriptData(
                video_id=video_id,
                language=transcript.language,
                is_generated=transcript.is_generated,
                segments=segments,
                full_text=full_text,
            )
            tlog.success()
            return GetVideoTranscriptResult(success=True, statusCode=200, data=data)
        except TranscriptsDisabled:
            msg = "Transcripts are disabled for this video"
            tlog.failure("TRANSCRIPTS_DISABLED", msg)
            return GetVideoTranscriptResult(
                success=False, statusCode=403, retriable=False,
                error=ToolError(code="TRANSCRIPTS_DISABLED", message=msg),
            )
        except NoTranscriptFound:
            msg = f"No transcript found for language(s): {languages}"
            tlog.failure("NO_TRANSCRIPT_FOUND", msg)
            return GetVideoTranscriptResult(
                success=False, statusCode=404, retriable=False,
                error=ToolError(code="NO_TRANSCRIPT_FOUND", message=msg),
            )
        except VideoUnavailable:
            msg = f"Video {video_id} is unavailable"
            tlog.failure("VIDEO_UNAVAILABLE", msg)
            return GetVideoTranscriptResult(
                success=False, statusCode=404, retriable=False,
                error=ToolError(code="VIDEO_UNAVAILABLE", message=msg),
            )
        except Exception as e:
            tlog.failure("SERVER_ERROR", str(e))
            return GetVideoTranscriptResult(
                success=False, statusCode=500, retriable=False,
                error=ToolError(code="SERVER_ERROR", message=str(e)),
            )

    @mcp.tool(
        name="list_video_transcripts",
        description=(
            "List all available transcript tracks for a YouTube video, including language, "
            "language code, whether the track is auto-generated, and whether it can be "
            "translated. Use this before get_video_transcript to discover available languages."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_video_transcripts(
        video_id: str = Field(..., description="YouTube video ID. Required."),
    ) -> ListVideoTranscriptsResult:
        tlog = ToolLogger(logger, "list_video_transcripts")
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            tracks = [
                TranscriptTrack(
                    language=t.language,
                    language_code=t.language_code,
                    is_generated=t.is_generated,
                    is_translatable=t.is_translatable,
                )
                for t in transcript_list
            ]
            data = TranscriptListData(video_id=video_id, tracks=tracks)
            tlog.success()
            return ListVideoTranscriptsResult(success=True, statusCode=200, data=data)
        except TranscriptsDisabled:
            msg = "Transcripts are disabled for this video"
            tlog.failure("TRANSCRIPTS_DISABLED", msg)
            return ListVideoTranscriptsResult(
                success=False, statusCode=403, retriable=False,
                error=ToolError(code="TRANSCRIPTS_DISABLED", message=msg),
            )
        except VideoUnavailable:
            msg = f"Video {video_id} is unavailable"
            tlog.failure("VIDEO_UNAVAILABLE", msg)
            return ListVideoTranscriptsResult(
                success=False, statusCode=404, retriable=False,
                error=ToolError(code="VIDEO_UNAVAILABLE", message=msg),
            )
        except Exception as e:
            tlog.failure("SERVER_ERROR", str(e))
            return ListVideoTranscriptsResult(
                success=False, statusCode=500, retriable=False,
                error=ToolError(code="SERVER_ERROR", message=str(e)),
            )
