import logging

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from fastmcp_credentials import get_credentials

logger = logging.getLogger("youtube-mcp-server")


def get_service():
    """Create YouTube service using credentials injected by fastmcp-credentials."""
    cred = get_credentials()
    if not cred.access_token:
        raise ValueError("No OAuth access token available in credentials")
    logger.info("Creating YouTube API service with provided access token")
    creds = Credentials(token=cred.access_token, scopes=cred.scopes)
    service = build("youtube", "v3", credentials=creds)
    logger.info("YouTube API service created successfully")
    return service
