"""Channels group: get_my_channel, get_my_playlists, get_my_subscriptions, get_my_activities, subscribe_to_channel."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from ..logging_utils import ToolLogger
from ..schemas import (
    GetMyActivitiesResult,
    GetMyChannelResult,
    GetMyPlaylistsResult,
    GetMySubscriptionsResult,
    SubscribeToChannelResult,
    YouTubeListData,
    YouTubeResourceData,
)
from ..service import get_service
from ._helpers import _handle_request_exc

logger = logging.getLogger("youtube-mcp.tools.channels")


def register_channels_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_my_channel",
        description=(
            "Get information about the authenticated user's YouTube channel. "
            "Returns snippet, contentDetails, and statistics for the channel."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_my_channel() -> GetMyChannelResult:
        tlog = ToolLogger(logger, "get_my_channel")
        try:
            service = get_service()
            response = service.channels().list(
                part="snippet,contentDetails,statistics",
                mine=True,
            ).execute()
            tlog.success()
            return GetMyChannelResult(success=True, statusCode=200, data=YouTubeListData(**response))
        except Exception as e:
            return _handle_request_exc(GetMyChannelResult, tlog, e)

    @mcp.tool(
        name="get_my_playlists",
        description=(
            "Get playlists from the authenticated user's channel. "
            "Returns snippet and contentDetails for each playlist."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_my_playlists(
        max_results: int = Field(default=25, description="Maximum playlists to return (capped at 50)"),
    ) -> GetMyPlaylistsResult:
        tlog = ToolLogger(logger, "get_my_playlists")
        try:
            service = get_service()
            response = service.playlists().list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=min(max_results, 50),
            ).execute()
            tlog.success()
            return GetMyPlaylistsResult(success=True, statusCode=200, data=YouTubeListData(**response))
        except Exception as e:
            return _handle_request_exc(GetMyPlaylistsResult, tlog, e)

    @mcp.tool(
        name="get_my_subscriptions",
        description=(
            "Get the authenticated user's channel subscriptions. "
            "Returns snippet and contentDetails for each subscription."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_my_subscriptions(
        max_results: int = Field(default=25, description="Maximum subscriptions to return (capped at 50)"),
    ) -> GetMySubscriptionsResult:
        tlog = ToolLogger(logger, "get_my_subscriptions")
        try:
            service = get_service()
            response = service.subscriptions().list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=min(max_results, 50),
            ).execute()
            tlog.success()
            return GetMySubscriptionsResult(success=True, statusCode=200, data=YouTubeListData(**response))
        except Exception as e:
            return _handle_request_exc(GetMySubscriptionsResult, tlog, e)

    @mcp.tool(
        name="get_my_activities",
        description=(
            "Get recent activities on the authenticated user's channel. "
            "Returns snippet and contentDetails for each activity."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_my_activities(
        max_results: int = Field(default=25, description="Maximum activities to return (capped at 50)"),
    ) -> GetMyActivitiesResult:
        tlog = ToolLogger(logger, "get_my_activities")
        try:
            service = get_service()
            response = service.activities().list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=min(max_results, 50),
            ).execute()
            tlog.success()
            return GetMyActivitiesResult(success=True, statusCode=200, data=YouTubeListData(**response))
        except Exception as e:
            return _handle_request_exc(GetMyActivitiesResult, tlog, e)

    @mcp.tool(
        name="subscribe_to_channel",
        description=(
            "Subscribe to a YouTube channel. "
            "Returns the created subscription resource including snippet details."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def subscribe_to_channel(
        channel_id: str = Field(..., description="Channel ID to subscribe to"),
    ) -> SubscribeToChannelResult:
        tlog = ToolLogger(logger, "subscribe_to_channel")
        try:
            service = get_service()
            response = service.subscriptions().insert(
                part="snippet",
                body={"snippet": {"resourceId": {"kind": "youtube#channel", "channelId": channel_id}}},
            ).execute()
            tlog.success()
            return SubscribeToChannelResult(success=True, statusCode=200, data=YouTubeResourceData(**response))
        except Exception as e:
            return _handle_request_exc(SubscribeToChannelResult, tlog, e)
