"""Upstream API client for MewCP YouTube MCP Server."""

import logging

from fastmcp_credentials import get_credentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger("youtube-mcp.service")


def get_service():
    cred = get_credentials()
    if not cred.access_token:
        raise ValueError("No OAuth access token available in credentials")
    creds = Credentials(
        token=cred.access_token,
    )
    return build("youtube", "v3", credentials=creds)
