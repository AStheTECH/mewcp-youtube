"""Pydantic schemas for MewCP YouTube MCP Server."""

from typing import Any

from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------------------------
# Base classes
# ---------------------------------------------------------------------------

class ToolError(BaseModel):
    code: str
    message: str
    details: Any = None


class ToolResult(BaseModel):
    success: bool
    statusCode: int
    retriable: bool = False
    retry_after_seconds: int | None = None
    error: ToolError | None = None


# ---------------------------------------------------------------------------
# YouTube list response data
# Used by: get_my_channel, get_my_playlists, search_videos, get_video_details,
#          get_channel_videos, get_playlist_items, get_video_comments,
#          get_my_subscriptions, get_my_activities
# ---------------------------------------------------------------------------

class YouTubeListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    kind: str | None = None
    etag: str | None = None
    nextPageToken: str | None = None
    prevPageToken: str | None = None
    items: list[dict[str, Any]] | None = None
    pageInfo: dict[str, Any] | None = None


class GetMyChannelResult(ToolResult):
    data: YouTubeListData | None = None


class GetMyPlaylistsResult(ToolResult):
    data: YouTubeListData | None = None


class SearchVideosResult(ToolResult):
    data: YouTubeListData | None = None


class GetVideoDetailsResult(ToolResult):
    data: YouTubeListData | None = None


class GetChannelVideosResult(ToolResult):
    data: YouTubeListData | None = None


class GetPlaylistItemsResult(ToolResult):
    data: YouTubeListData | None = None


class GetVideoCommentsResult(ToolResult):
    data: YouTubeListData | None = None


class GetMySubscriptionsResult(ToolResult):
    data: YouTubeListData | None = None


class GetMyActivitiesResult(ToolResult):
    data: YouTubeListData | None = None


# ---------------------------------------------------------------------------
# YouTube resource response data
# Used by: create_playlist, add_video_to_playlist, subscribe_to_channel,
#          post_comment
# ---------------------------------------------------------------------------

class YouTubeResourceData(BaseModel):
    model_config = ConfigDict(extra="allow")

    kind: str | None = None
    etag: str | None = None
    id: str | None = None
    snippet: dict[str, Any] | None = None
    contentDetails: dict[str, Any] | None = None
    statistics: dict[str, Any] | None = None
    status: dict[str, Any] | None = None


class CreatePlaylistResult(ToolResult):
    data: YouTubeResourceData | None = None


class AddVideoToPlaylistResult(ToolResult):
    data: YouTubeResourceData | None = None


class SubscribeToChannelResult(ToolResult):
    data: YouTubeResourceData | None = None


class PostCommentResult(ToolResult):
    data: YouTubeResourceData | None = None


# ---------------------------------------------------------------------------
# Message-only response data
# Used by: rate_video
# ---------------------------------------------------------------------------

class MessageData(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str


class RateVideoResult(ToolResult):
    data: MessageData | None = None


# ---------------------------------------------------------------------------
# Transcript data
# Used by: get_video_transcript, list_video_transcripts
# ---------------------------------------------------------------------------

class TranscriptSegment(BaseModel):
    model_config = ConfigDict(extra="allow")

    text: str
    start: float
    duration: float


class TranscriptData(BaseModel):
    model_config = ConfigDict(extra="allow")

    video_id: str
    language: str
    is_generated: bool
    segments: list[TranscriptSegment]
    full_text: str


class TranscriptTrack(BaseModel):
    model_config = ConfigDict(extra="allow")

    language: str
    language_code: str
    is_generated: bool
    is_translatable: bool


class TranscriptListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    video_id: str
    tracks: list[TranscriptTrack]


class GetVideoTranscriptResult(ToolResult):
    data: TranscriptData | None = None


class ListVideoTranscriptsResult(ToolResult):
    data: TranscriptListData | None = None
