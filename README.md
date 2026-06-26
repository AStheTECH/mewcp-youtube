**Your YouTube, fully accessible through AI.**

A Model Context Protocol (MCP) server that exposes YouTube's API for searching videos, managing playlists, reading channel data, posting comments, and more.


## Overview

The MewCP YouTube MCP Server provides authenticated access to the YouTube Data API v3:

- Search and retrieve videos, channel data, and comments
- Manage playlists: create, browse, and add videos
- Interact with content: rate videos, post comments, subscribe to channels

Perfect for:

- Building AI assistants that can search and analyze YouTube content
- Automating YouTube channel management tasks
- Integrating YouTube data into workflows and dashboards


## Tools


<details>
<summary><code>get_my_channel</code> — Get the authenticated user's YouTube channel info</summary>

Get information about the authenticated user's YouTube channel. Returns snippet, contentDetails, and statistics for the channel.

**Inputs:**
```
(no parameters)
```

**Output `data` schema:**

```typescript
{
  kind: string | null;
  etag: string | null;
  nextPageToken: string | null;
  prevPageToken: string | null;
  items: object[] | null;
  pageInfo: object | null;
}
```

</details>


<details>
<summary><code>get_my_playlists</code> — Get playlists from the authenticated user's channel</summary>

Get playlists from the authenticated user's channel. Returns snippet and contentDetails for each playlist.

**Inputs:**
```
- `max_results` (int, optional, default: 25) — Maximum playlists to return (capped at 50). Defaults to 25.
```

**Output `data` schema:**

```typescript
{
  kind: string | null;
  etag: string | null;
  nextPageToken: string | null;
  prevPageToken: string | null;
  items: object[] | null;
  pageInfo: object | null;
}
```

</details>


<details>
<summary><code>get_my_subscriptions</code> — Get the authenticated user's channel subscriptions</summary>

Get the authenticated user's channel subscriptions. Returns snippet and contentDetails for each subscription.

**Inputs:**
```
- `max_results` (int, optional, default: 25) — Maximum subscriptions to return (capped at 50). Defaults to 25.
```

**Output `data` schema:**

```typescript
{
  kind: string | null;
  etag: string | null;
  nextPageToken: string | null;
  prevPageToken: string | null;
  items: object[] | null;
  pageInfo: object | null;
}
```

</details>


<details>
<summary><code>get_my_activities</code> — Get recent activities on the authenticated user's channel</summary>

Get recent activities on the authenticated user's channel. Returns snippet and contentDetails for each activity.

**Inputs:**
```
- `max_results` (int, optional, default: 25) — Maximum activities to return (capped at 50). Defaults to 25.
```

**Output `data` schema:**

```typescript
{
  kind: string | null;
  etag: string | null;
  nextPageToken: string | null;
  prevPageToken: string | null;
  items: object[] | null;
  pageInfo: object | null;
}
```

</details>


<details>
<summary><code>subscribe_to_channel</code> — Subscribe to a YouTube channel</summary>

Subscribe to a YouTube channel. Returns the created subscription resource including snippet details.

**Inputs:**
```
- `channel_id` (str, required) — Channel ID to subscribe to. Required.
```

**Output `data` schema:**

```typescript
{
  kind: string | null;
  etag: string | null;
  id: string | null;
  snippet: object | null;
  contentDetails: object | null;
  statistics: object | null;
  status: object | null;
}
```

</details>


<details>
<summary><code>search_videos</code> — Search for videos on YouTube</summary>

Search for videos on YouTube.

**Inputs:**
```
- `query` (str, required) — Search query text. Required.
- `max_results` (int, optional, default: 10) — Maximum videos to return (capped at 50). Defaults to 10.
- `order` (str, optional, default: "relevance") — Sort order. Common values: `relevance`, `date`, `rating`, `title`, `videoCount`, `viewCount`. Defaults to `relevance`.
```

**Output `data` schema:**

```typescript
{
  kind: string | null;
  etag: string | null;
  nextPageToken: string | null;
  prevPageToken: string | null;
  items: object[] | null;
  pageInfo: object | null;
}
```

</details>


<details>
<summary><code>get_video_details</code> — Get detailed information about a specific video</summary>

Get detailed information about a specific video by ID.

**Inputs:**
```
- `video_id` (str, required) — YouTube video ID. Required.
```

**Output `data` schema:**

```typescript
{
  kind: string | null;
  etag: string | null;
  nextPageToken: string | null;
  prevPageToken: string | null;
  items: object[] | null;
  pageInfo: object | null;
}
```

</details>


<details>
<summary><code>get_channel_videos</code> — Get videos from a specific channel</summary>

Get videos from a specific channel.

**Inputs:**
```
- `channel_id` (str, required) — YouTube channel ID. Required.
- `max_results` (int, optional, default: 25) — Maximum videos to return (capped at 50). Defaults to 25.
```

**Output `data` schema:**

```typescript
{
  kind: string | null;
  etag: string | null;
  nextPageToken: string | null;
  prevPageToken: string | null;
  items: object[] | null;
  pageInfo: object | null;
}
```

</details>


<details>
<summary><code>get_video_comments</code> — Get comments for a specific video</summary>

Get comments for a specific video.

**Inputs:**
```
- `video_id` (str, required) — YouTube video ID. Required.
- `max_results` (int, optional, default: 20) — Maximum comments to return (capped at 100). Defaults to 20.
- `order` (str, optional, default: "relevance") — Comment order. Supported values: `relevance`, `time`. Defaults to `relevance`.
```

**Output `data` schema:**

```typescript
{
  kind: string | null;
  etag: string | null;
  nextPageToken: string | null;
  prevPageToken: string | null;
  items: object[] | null;
  pageInfo: object | null;
}
```

</details>


<details>
<summary><code>post_comment</code> — Post a comment on a video</summary>

Post a comment on a video.

**Inputs:**
```
- `video_id` (str, required) — YouTube video ID. Required.
- `text` (str, required) — Comment text content. Required.
```

**Output `data` schema:**

```typescript
{
  kind: string | null;
  etag: string | null;
  id: string | null;
  snippet: object | null;
  contentDetails: object | null;
  statistics: object | null;
  status: object | null;
}
```

</details>


<details>
<summary><code>rate_video</code> — Rate a video (like or dislike)</summary>

Rate a video (like or dislike).

**Inputs:**
```
- `video_id` (str, required) — YouTube video ID. Required.
- `rating` ("like" | "dislike" | "none", required) — Rating value: `like`, `dislike`, or `none` (removes rating). Required.
```

**Output `data` schema:**

```typescript
{
  message: string;
}
```

</details>


<details>
<summary><code>get_playlist_items</code> — Get videos from a specific playlist</summary>

Get videos from a specific playlist.

**Inputs:**
```
- `playlist_id` (str, required) — YouTube playlist ID. Required.
- `max_results` (int, optional, default: 50) — Maximum items to return (capped at 50). Defaults to 50.
```

**Output `data` schema:**

```typescript
{
  kind: string | null;
  etag: string | null;
  nextPageToken: string | null;
  prevPageToken: string | null;
  items: object[] | null;
  pageInfo: object | null;
}
```

</details>


<details>
<summary><code>create_playlist</code> — Create a new playlist on the authenticated user's channel</summary>

Create a new playlist on the authenticated user's channel.

**Inputs:**
```
- `title` (str, required) — Playlist title. Required.
- `description` (str, optional, default: "") — Optional playlist description. Defaults to empty string.
- `privacy_status` (str, optional, default: "private") — Privacy setting. Common values: `private`, `public`, `unlisted`. Defaults to `private`.
```

**Output `data` schema:**

```typescript
{
  kind: string | null;
  etag: string | null;
  id: string | null;
  snippet: object | null;
  contentDetails: object | null;
  statistics: object | null;
  status: object | null;
}
```

</details>


<details>
<summary><code>add_video_to_playlist</code> — Add a video to a playlist</summary>

Add a video to a playlist.

**Inputs:**
```
- `playlist_id` (str, required) — Target playlist ID. Required.
- `video_id` (str, required) — Video ID to insert. Required.
```

**Output `data` schema:**

```typescript
{
  kind: string | null;
  etag: string | null;
  id: string | null;
  snippet: object | null;
  contentDetails: object | null;
  statistics: object | null;
  status: object | null;
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Response Envelope</strong></summary>

Every tool returns the same top-level envelope. Only `data` varies per tool.

```json
// Success
{
  "success": true,
  "statusCode": 200,
  "retriable": false,
  "retry_after_seconds": null,
  "error": null,
  "data": { ... }
}

// Error
{
  "success": false,
  "statusCode": 400,
  "retriable": false,
  "retry_after_seconds": null,
  "error": { "code": "ERROR_CODE", "message": "description", "details": {} },
  "data": null
}
```

- `retriable` — `true` when it is safe to retry (rate limit, network error, 503). `false` for validation and auth errors.
- `retry_after_seconds` — seconds to wait before retrying; present only when `retriable` is `true` and the upstream specifies a delay.
- `error.code` — machine-readable string: `VALIDATION_ERROR`, `AUTH_ERROR`, `UPSTREAM_ERROR`, `SERVER_ERROR`.

</details>

<details>
<summary><strong>Common Parameters</strong></summary>

- `max_results` — Controls the number of items returned. Always capped at the YouTube API maximum for the given endpoint (50 for most resources, 100 for comments).
- `order` — Controls result ordering. Supported values vary by tool; see each tool's parameter description for the accepted values.

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**Video ID:**

```
11-character alphanumeric string
Example: dQw4w9WgXcQ
```

**Channel ID:**

```
Starts with "UC" followed by 22 characters
Example: UCq-Fj5jknLsUf-MWSy4_brA
```

**Playlist ID:**

```
Starts with "PL" followed by alphanumeric characters
Example: PLbpi6ZahtOH6Ar_3GPy3workbp73xONIf
```

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** OAuth token not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_OAUTH_TOKEN` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check that your OAuth credential is active in your MewCP account

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
  2. Connect your Google/YouTube account via OAuth
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

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
  1. Check YouTube service status at [Google Workspace Status](https://www.google.com/appsstatus)
  2. Verify your OAuth credential has the required YouTube scopes
  3. Review the error message for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[YouTube Data API Documentation](https://developers.google.com/youtube/v3/docs)** — Official API reference
- **[YouTube Data API Reference](https://developers.google.com/youtube/v3/docs/videos/list)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling


</details>
