"""Playlists group: get_playlist_items, create_playlist, add_video_to_playlist."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from ..logging_utils import ToolLogger
from ..schemas import (
    AddVideoToPlaylistResult,
    CreatePlaylistResult,
    GetPlaylistItemsResult,
    YouTubeListData,
    YouTubeResourceData,
)
from ..service import get_service
from ._helpers import _handle_request_exc

logger = logging.getLogger("youtube-mcp.tools.playlists")


def register_playlists_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_playlist_items",
        description="Get videos from a specific playlist.",
        annotations=ToolAnnotations(
            readOnlyHint=True, destructiveHint=False, openWorldHint=True
        ),
    )
    def get_playlist_items(
        playlist_id: str = Field(..., description="YouTube playlist ID"),
        max_results: int = Field(
            default=50, description="Maximum items to return (capped at 50)"
        ),
    ) -> GetPlaylistItemsResult:
        tlog = ToolLogger(logger, "get_playlist_items")
        try:
            service = get_service()
            response = service.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=min(max_results, 50),
            ).execute()
            tlog.success()
            return GetPlaylistItemsResult(
                success=True, statusCode=200, data=YouTubeListData(**response)
            )
        except Exception as exc:
            return _handle_request_exc(GetPlaylistItemsResult, tlog, exc)

    @mcp.tool(
        name="create_playlist",
        description="Create a new playlist on the authenticated user's channel.",
        annotations=ToolAnnotations(
            readOnlyHint=False, destructiveHint=False, openWorldHint=True
        ),
    )
    def create_playlist(
        title: str = Field(..., description="Playlist title"),
        description: str = Field(
            default="", description="Optional playlist description"
        ),
        privacy_status: str = Field(
            default="private",
            description="Privacy setting. Common values: `private`, `public`, `unlisted`",
        ),
    ) -> CreatePlaylistResult:
        tlog = ToolLogger(logger, "create_playlist")
        try:
            service = get_service()
            response = service.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {"title": title, "description": description},
                    "status": {"privacyStatus": privacy_status},
                },
            ).execute()
            tlog.success()
            return CreatePlaylistResult(
                success=True, statusCode=200, data=YouTubeResourceData(**response)
            )
        except Exception as exc:
            return _handle_request_exc(CreatePlaylistResult, tlog, exc)

    @mcp.tool(
        name="add_video_to_playlist",
        description="Add a video to a playlist.",
        annotations=ToolAnnotations(
            readOnlyHint=False, destructiveHint=False, openWorldHint=True
        ),
    )
    def add_video_to_playlist(
        playlist_id: str = Field(..., description="Target playlist ID"),
        video_id: str = Field(..., description="Video ID to insert"),
    ) -> AddVideoToPlaylistResult:
        tlog = ToolLogger(logger, "add_video_to_playlist")
        try:
            service = get_service()
            response = service.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {"kind": "youtube#video", "videoId": video_id},
                    }
                },
            ).execute()
            tlog.success()
            return AddVideoToPlaylistResult(
                success=True, statusCode=200, data=YouTubeResourceData(**response)
            )
        except Exception as exc:
            return _handle_request_exc(AddVideoToPlaylistResult, tlog, exc)
