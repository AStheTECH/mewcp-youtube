"""Videos group: search_videos, get_video_details, get_channel_videos, get_video_comments, post_comment, rate_video."""

import logging
from typing import Literal

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from ..logging_utils import ToolLogger
from ..schemas import (
    GetChannelVideosResult,
    GetVideoCommentsResult,
    GetVideoDetailsResult,
    MessageData,
    PostCommentResult,
    RateVideoResult,
    SearchVideosResult,
    YouTubeListData,
    YouTubeResourceData,
)
from ..service import get_service
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("youtube-mcp.tools.videos")


def register_videos_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="search_videos",
        description="Search for videos on YouTube.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def search_videos(
        query: str = Field(..., description="Search query text. Required."),
        max_results: int = Field(default=10, description="Maximum videos to return (capped at 50). Defaults to 10."),
        order: str = Field(
            default="relevance",
            description="Sort order. Common values: `relevance`, `date`, `rating`, `title`, `videoCount`, `viewCount`. Defaults to `relevance`.",
        ),
    ) -> SearchVideosResult:
        tlog = ToolLogger(logger, "search_videos")
        try:
            service = get_service()
            request = service.search().list(
                part="snippet",
                q=query,
                type="video",
                maxResults=min(max_results, 50),
                order=order,
            )
            response = request.execute()
            tlog.success()
            return SearchVideosResult(success=True, statusCode=200, data=YouTubeListData(**response))
        except Exception as e:
            return _handle_request_exc(SearchVideosResult, tlog, e)

    @mcp.tool(
        name="get_video_details",
        description="Get detailed information about a specific video by ID.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_video_details(
        video_id: str = Field(..., description="YouTube video ID. Required."),
    ) -> GetVideoDetailsResult:
        tlog = ToolLogger(logger, "get_video_details")
        try:
            service = get_service()
            request = service.videos().list(
                part="snippet,contentDetails,statistics,status",
                id=video_id,
            )
            response = request.execute()
            tlog.success()
            return GetVideoDetailsResult(success=True, statusCode=200, data=YouTubeListData(**response))
        except Exception as e:
            return _handle_request_exc(GetVideoDetailsResult, tlog, e)

    @mcp.tool(
        name="get_channel_videos",
        description="Get videos from a specific channel.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_channel_videos(
        channel_id: str = Field(..., description="YouTube channel ID. Required."),
        max_results: int = Field(default=25, description="Maximum videos to return (capped at 50). Defaults to 25."),
    ) -> GetChannelVideosResult:
        tlog = ToolLogger(logger, "get_channel_videos")
        try:
            service = get_service()
            request = service.search().list(
                part="snippet",
                channelId=channel_id,
                type="video",
                maxResults=min(max_results, 50),
                order="date",
            )
            response = request.execute()
            tlog.success()
            return GetChannelVideosResult(success=True, statusCode=200, data=YouTubeListData(**response))
        except Exception as e:
            return _handle_request_exc(GetChannelVideosResult, tlog, e)

    @mcp.tool(
        name="get_video_comments",
        description="Get comments for a specific video.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_video_comments(
        video_id: str = Field(..., description="YouTube video ID. Required."),
        max_results: int = Field(default=20, description="Maximum comments to return (capped at 100). Defaults to 20."),
        order: str = Field(
            default="relevance",
            description="Comment order. Supported values: `relevance`, `time`. Defaults to `relevance`.",
        ),
    ) -> GetVideoCommentsResult:
        tlog = ToolLogger(logger, "get_video_comments")
        try:
            service = get_service()
            request = service.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=min(max_results, 100),
                order=order,
            )
            response = request.execute()
            tlog.success()
            return GetVideoCommentsResult(success=True, statusCode=200, data=YouTubeListData(**response))
        except Exception as e:
            return _handle_request_exc(GetVideoCommentsResult, tlog, e)

    @mcp.tool(
        name="post_comment",
        description="Post a comment on a video.",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def post_comment(
        video_id: str = Field(..., description="YouTube video ID. Required."),
        text: str = Field(..., description="Comment text content. Required."),
    ) -> PostCommentResult:
        tlog = ToolLogger(logger, "post_comment")
        try:
            service = get_service()
            request = service.commentThreads().insert(
                part="snippet",
                body={
                    "snippet": {
                        "videoId": video_id,
                        "topLevelComment": {
                            "snippet": {
                                "textOriginal": text,
                            }
                        },
                    }
                },
            )
            response = request.execute()
            tlog.success()
            return PostCommentResult(success=True, statusCode=200, data=YouTubeResourceData(**response))
        except Exception as e:
            return _handle_request_exc(PostCommentResult, tlog, e)

    @mcp.tool(
        name="rate_video",
        description="Rate a video (like or dislike).",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def rate_video(
        video_id: str = Field(..., description="YouTube video ID. Required."),
        rating: Literal["like", "dislike", "none"] = Field(..., description="Rating value: `like`, `dislike`, or `none` (removes rating). Required."),
    ) -> RateVideoResult:
        tlog = ToolLogger(logger, "rate_video")
        try:
            service = get_service()
            request = service.videos().rate(id=video_id, rating=rating)
            request.execute()
            tlog.success()
            return RateVideoResult(
                success=True,
                statusCode=200,
                data=MessageData(message=f"Video rated as '{rating}' successfully"),
            )
        except Exception as e:
            return _handle_request_exc(RateVideoResult, tlog, e)
