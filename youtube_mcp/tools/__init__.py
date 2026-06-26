from fastmcp import FastMCP

from .channels_tools import register_channels_tools
from .videos_tools import register_videos_tools
from .playlists_tools import register_playlists_tools
from .transcripts_tools import register_transcripts_tools


def register_tools(mcp: FastMCP) -> None:
    register_channels_tools(mcp)
    register_videos_tools(mcp)
    register_playlists_tools(mcp)
    register_transcripts_tools(mcp)
