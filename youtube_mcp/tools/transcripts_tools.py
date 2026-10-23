"""Transcripts group: get_video_transcript, list_video_transcripts."""

import logging
from typing import Optional

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    AgeRestricted,
    InvalidVideoId,
    IpBlocked,
    RequestBlocked,
    TranscriptsDisabled,
    VideoUnavailable,
    VideoUnplayable,
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

_ERRORS = (
    (TranscriptsDisabled, "TRANSCRIPTS_DISABLED", 403, False, "Transcripts are disabled for this video"),
    (InvalidVideoId, "INVALID_VIDEO_ID", 400, False, "Invalid video ID; pass the 11-character ID, not a URL"),
    (VideoUnavailable, "VIDEO_UNAVAILABLE", 404, False, "Video is unavailable"),
    (AgeRestricted, "AGE_RESTRICTED", 403, False, "Video is age-restricted and its transcript cannot be fetched"),
    (VideoUnplayable, "VIDEO_UNPLAYABLE", 403, False, "Video is not playable, so no transcript can be fetched"),
    (IpBlocked, "UPSTREAM_BLOCKED", 429, True, "YouTube blocked the transcript request from this server's IP"),
    (RequestBlocked, "UPSTREAM_BLOCKED", 429, True, "YouTube blocked the transcript request"),
)


def _transcript_failure(result_class, tlog, exc):
    for exc_type, code, status, retriable, msg in _ERRORS:
        if isinstance(exc, exc_type):
            tlog.failure(code, msg)
            return result_class(
                success=False, statusCode=status, retriable=retriable,
                error=ToolError(code=code, message=msg),
            )
    tlog.failure("SERVER_ERROR", str(exc))
    return result_class(
        success=False, statusCode=500, retriable=False,
        error=ToolError(code="SERVER_ERROR", message=str(exc)),
    )


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
            transcript_list = YouTubeTranscriptApi().list(video_id)
            transcript = None
            if languages:
                try:
                    transcript = transcript_list.find_transcript(languages)
                except Exception:
                    transcript = None
            if transcript is None:
                transcript = next(iter(transcript_list), None)
            if transcript is None:
                msg = "No transcript available for this video"
                tlog.failure("NO_TRANSCRIPT_FOUND", msg)
                return GetVideoTranscriptResult(
                    success=False, statusCode=404, retriable=False,
                    error=ToolError(code="NO_TRANSCRIPT_FOUND", message=msg),
                )

            fetched = transcript.fetch()
            segments = [
                TranscriptSegment(text=s.text, start=s.start, duration=s.duration)
                for s in fetched
            ]
            data = TranscriptData(
                video_id=video_id,
                language=transcript.language,
                is_generated=transcript.is_generated,
                segments=segments,
                full_text=" ".join(s.text for s in fetched),
            )
            tlog.success()
            return GetVideoTranscriptResult(success=True, statusCode=200, data=data)
        except Exception as e:
            return _transcript_failure(GetVideoTranscriptResult, tlog, e)

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
            transcript_list = YouTubeTranscriptApi().list(video_id)
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
        except Exception as e:
            return _transcript_failure(ListVideoTranscriptsResult, tlog, e)
