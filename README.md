**Your YouTube channel and content, fully accessible through AI.**

A Model Context Protocol (MCP) server that exposes YouTube's Data API for searching videos, managing playlists, reading comments, and interacting with channel content.


## Overview

The YouTube MCP Server provides comprehensive access to YouTube via the authenticated user's account:

- Search videos, fetch channel info, playlists, and subscriptions
- Read video details, comments, and channel activity
- Create playlists, add videos, post comments, rate videos, and subscribe to channels

Perfect for:

- AI assistants that need to search or retrieve YouTube content on your behalf
- Automating playlist management and channel organization
- Building tools that integrate YouTube data into broader workflows


## Tools

### Channel & Account

<details>
<summary><code>get_my_channel</code> — Get authenticated user's channel info</summary>

Returns snippet, content details, and statistics for the authenticated user's YouTube channel.

**Inputs:**
```
None
```

**Output:**

```json
{
  "kind": "youtube#channelListResponse",
  "items": [{
    "id": "UC...",
    "snippet": { "title": "My Channel", "description": "..." },
    "statistics": { "viewCount": "12000", "subscriberCount": "500" }
  }]
}
```

</details>


<details>
<summary><code>get_my_playlists</code> — Get playlists from the authenticated user's channel</summary>

Returns playlists owned by the authenticated user with snippet and content details.

**Inputs:**
```
- `max_results` (int, optional) — Maximum playlists to return (max: 50, default: 25)
```

**Output:**

```json
{
  "kind": "youtube#playlistListResponse",
  "pageInfo": { "totalResults": 5, "resultsPerPage": 25 },
  "items": [{ "id": "PL...", "snippet": { "title": "My Playlist", "itemCount": 10 } }]
}
```

</details>


<details>
<summary><code>get_my_subscriptions</code> — Get the authenticated user's subscriptions</summary>

Returns channels the authenticated user is subscribed to, with snippet and content details.

**Inputs:**
```
- `max_results` (int, optional) — Maximum subscriptions to return (max: 50, default: 25)
```

**Output:**

```json
{
  "kind": "youtube#subscriptionListResponse",
  "items": [{
    "snippet": {
      "title": "Channel Name",
      "resourceId": { "channelId": "UC..." }
    }
  }]
}
```

</details>


<details>
<summary><code>get_my_activities</code> — Get recent activities on the authenticated user's channel</summary>

Returns recent activity events on the authenticated user's channel such as uploads, likes, and subscriptions.

**Inputs:**
```
- `max_results` (int, optional) — Maximum activities to return (max: 50, default: 25)
```

**Output:**

```json
{
  "kind": "youtube#activityListResponse",
  "items": [{
    "snippet": { "type": "upload", "publishedAt": "2024-01-15T..." },
    "contentDetails": { "upload": { "videoId": "abc123" } }
  }]
}
```

</details>


### Videos

<details>
<summary><code>search_videos</code> — Search for videos on YouTube</summary>

Searches YouTube for videos matching a query, with configurable sort order and result count.

**Inputs:**
```
- `query` (string, required) — Search query text
- `max_results` (int, optional) — Maximum videos to return (max: 50, default: 10)
- `order` (string, optional) — Sort order: relevance, date, rating, title, videoCount, or viewCount (default: relevance)
```

**Output:**

```json
{
  "kind": "youtube#searchListResponse",
  "pageInfo": { "totalResults": 1000000 },
  "items": [{
    "id": { "videoId": "dQw4w9WgXcQ" },
    "snippet": { "title": "Video Title", "channelTitle": "Channel Name", "publishedAt": "..." }
  }]
}
```

</details>


<details>
<summary><code>get_video_details</code> — Get detailed information about a video</summary>

Returns full details for a specific video including snippet, content details, statistics, and status.

**Inputs:**
```
- `video_id` (string, required) — YouTube video ID (e.g., dQw4w9WgXcQ)
```

**Output:**

```json
{
  "kind": "youtube#videoListResponse",
  "items": [{
    "id": "dQw4w9WgXcQ",
    "snippet": { "title": "...", "description": "...", "publishedAt": "..." },
    "statistics": { "viewCount": "1500000", "likeCount": "50000" },
    "contentDetails": { "duration": "PT3M33S" },
    "status": { "privacyStatus": "public" }
  }]
}
```

</details>


<details>
<summary><code>get_channel_videos</code> — Get videos from a specific channel</summary>

Returns the most recent videos uploaded to a channel, sorted by date.

**Inputs:**
```
- `channel_id` (string, required) — YouTube channel ID (e.g., UCxxxxxx)
- `max_results` (int, optional) — Maximum videos to return (max: 50, default: 25)
```

**Output:**

```json
{
  "kind": "youtube#searchListResponse",
  "items": [{
    "id": { "videoId": "abc123" },
    "snippet": { "title": "Latest Video", "publishedAt": "2024-01-15T..." }
  }]
}
```

</details>


<details>
<summary><code>get_video_comments</code> — Get comments for a video</summary>

Returns comment threads for a specific video, with optional ordering by relevance or time.

**Inputs:**
```
- `video_id` (string, required) — YouTube video ID
- `max_results` (int, optional) — Maximum comments to return (max: 100, default: 20)
- `order` (string, optional) — Comment order: relevance or time (default: relevance)
```

**Output:**

```json
{
  "kind": "youtube#commentThreadListResponse",
  "items": [{
    "snippet": {
      "topLevelComment": {
        "snippet": { "textDisplay": "Great video!", "likeCount": 42, "authorDisplayName": "..." }
      },
      "totalReplyCount": 3
    }
  }]
}
```

</details>


<details>
<summary><code>rate_video</code> — Like, dislike, or remove a rating from a video</summary>

Rates a video on behalf of the authenticated user.

**Inputs:**
```
- `video_id` (string, required) — YouTube video ID
- `rating` (string, required) — Rating value: like, dislike, or none
```

**Output:**

```json
{
  "message": "Video rated as 'like' successfully"
}
```

</details>


<details>
<summary><code>post_comment</code> — Post a comment on a video</summary>

Posts a top-level comment on a video on behalf of the authenticated user.

**Inputs:**
```
- `video_id` (string, required) — YouTube video ID
- `text` (string, required) — Comment text content
```

**Output:**

```json
{
  "kind": "youtube#commentThread",
  "id": "comment-thread-id",
  "snippet": {
    "topLevelComment": { "snippet": { "textOriginal": "Great video!", "publishedAt": "..." } }
  }
}
```

</details>


### Playlists

<details>
<summary><code>get_playlist_items</code> — Get videos from a playlist</summary>

Returns the videos inside a specific playlist with snippet and content details.

**Inputs:**
```
- `playlist_id` (string, required) — YouTube playlist ID (e.g., PLxxxxxx)
- `max_results` (int, optional) — Maximum items to return (max: 50, default: 50)
```

**Output:**

```json
{
  "kind": "youtube#playlistItemListResponse",
  "pageInfo": { "totalResults": 20 },
  "items": [{
    "snippet": { "title": "Video Title", "position": 0, "resourceId": { "videoId": "abc123" } }
  }]
}
```

</details>


<details>
<summary><code>create_playlist</code> — Create a new playlist</summary>

Creates a new playlist on the authenticated user's channel with a specified title, description, and privacy setting.

**Inputs:**
```
- `title` (string, required) — Playlist title
- `description` (string, optional) — Playlist description (default: "")
- `privacy_status` (string, optional) — Privacy setting: private, public, or unlisted (default: private)
```

**Output:**

```json
{
  "kind": "youtube#playlist",
  "id": "PL...",
  "snippet": { "title": "My New Playlist", "description": "..." },
  "status": { "privacyStatus": "private" }
}
```

</details>


<details>
<summary><code>add_video_to_playlist</code> — Add a video to a playlist</summary>

Adds an existing video to one of the authenticated user's playlists.

**Inputs:**
```
- `playlist_id` (string, required) — Target playlist ID
- `video_id` (string, required) — Video ID to add
```

**Output:**

```json
{
  "kind": "youtube#playlistItem",
  "id": "playlist-item-id",
  "snippet": { "playlistId": "PL...", "resourceId": { "videoId": "abc123" }, "position": 5 }
}
```

</details>


### Subscriptions

<details>
<summary><code>subscribe_to_channel</code> — Subscribe to a YouTube channel</summary>

Subscribes the authenticated user to a specified YouTube channel.

**Inputs:**
```
- `channel_id` (string, required) — YouTube channel ID to subscribe to (e.g., UCxxxxxx)
```

**Output:**

```json
{
  "kind": "youtube#subscription",
  "id": "subscription-id",
  "snippet": {
    "title": "Channel Name",
    "resourceId": { "channelId": "UC..." }
  }
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>YouTube ID Formats</strong></summary>

| Resource | Format | Example |
|---|---|---|
| Video ID | 11-character alphanumeric | `dQw4w9WgXcQ` |
| Channel ID | Starts with `UC` | `UCxxxxxxxxxxxxxxxxxxxxxx` |
| Playlist ID | Starts with `PL` | `PLxxxxxxxxxxxxxxxxxxxxxx` |

IDs can be found in YouTube URLs:
```
Video:    https://youtube.com/watch?v=dQw4w9WgXcQ  → dQw4w9WgXcQ
Channel:  https://youtube.com/channel/UCxxxxxx      → UCxxxxxx
Playlist: https://youtube.com/playlist?list=PLxxxxx → PLxxxxx
```

</details>

<details>
<summary><strong>Search Order Options</strong></summary>

The `order` parameter in `search_videos` accepts:

- `relevance` — Ranked by relevance to the query (default)
- `date` — Most recently published first
- `rating` — Highest rated first
- `viewCount` — Most viewed first
- `title` — Alphabetical by title
- `videoCount` — For channel searches: most videos first

</details>

<details>
<summary><strong>Privacy Status Options</strong></summary>

Used in `create_playlist`:

- `private` — Only visible to you (default)
- `public` — Visible to everyone
- `unlisted` — Visible to anyone with the link

</details>

<details>
<summary><strong>Video Duration Format</strong></summary>

Durations in `contentDetails` use ISO 8601 format:

```
PT3M33S  → 3 minutes, 33 seconds
PT1H2M   → 1 hour, 2 minutes
PT45S    → 45 seconds
```

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** OAuth token not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_TOKEN` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check your YouTube OAuth credential is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No YouTube credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Connect your Google account via OAuth (YouTube scope)
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values (e.g. `max_results` must be an integer)

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>YouTube API Error</strong></summary>

- **Cause:** Upstream YouTube Data API returned an error
- **Solution:**
  1. Check Google service status at [Google Status](https://status.cloud.google.com)
  2. Verify your OAuth credential has the required YouTube scopes (e.g. `youtube.readonly`, `youtube.force-ssl`)
  3. Review the error message returned in the response — common errors: `quotaExceeded`, `forbidden`, `videoNotFound`

</details>

---

### Resources

- **[YouTube Data API Documentation](https://developers.google.com/youtube/v3)** — Official API reference
- **[YouTube Data API Reference](https://developers.google.com/youtube/v3/docs)** — Complete method reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling
