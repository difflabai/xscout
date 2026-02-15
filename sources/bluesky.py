"""Bluesky source adapter — uses Bluesky's public search API (no auth required)."""

import json
import sys
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .base import Post, SourceAdapter

USER_AGENT = "xscout/1.0 (local-ai-scout; stdlib)"

# Public API — be polite
_MIN_REQUEST_INTERVAL = 1.0  # seconds between requests
_last_request_time = 0.0


def _rate_limit():
    """Sleep if needed to stay polite with the public API."""
    global _last_request_time
    now = time.monotonic()
    elapsed = now - _last_request_time
    if elapsed < _MIN_REQUEST_INTERVAL:
        time.sleep(_MIN_REQUEST_INTERVAL - elapsed)
    _last_request_time = time.monotonic()


def _bsky_get(url: str) -> dict:
    """Fetch a Bluesky public API endpoint with rate limiting."""
    _rate_limit()
    req = Request(url)
    req.add_header("User-Agent", USER_AGENT)
    req.add_header("Accept", "application/json")
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"  ⚠ Bluesky request failed: {e}", file=sys.stderr)
        return {}


class BlueskyAdapter(SourceAdapter):
    @property
    def name(self) -> str:
        return "bluesky"

    def fetch(self, topic: str, lookback_hours: int = 24, max_results: int = 100,
              queries: list[str] | None = None) -> list[Post]:
        search_terms = self._build_search_terms(topic, queries)
        since = (datetime.now(timezone.utc) - timedelta(hours=lookback_hours)).strftime("%Y-%m-%dT%H:%M:%SZ")

        posts: list[Post] = []
        seen_uris: set[str] = set()

        for i, term in enumerate(search_terms, 1):
            print(f"  [bluesky {i}/{len(search_terms)}] {term[:50]}...", file=sys.stderr)
            results = self._search(term, since, max_results)
            for post in results:
                if post.url not in seen_uris:
                    seen_uris.add(post.url)
                    posts.append(post)

        print(f"  -> {len(posts)} posts from Bluesky", file=sys.stderr)
        return posts

    def _build_search_terms(self, topic: str, queries: list[str] | None) -> list[str]:
        """Build search terms from topic string.

        Split comma-separated topics into separate searches.
        """
        if queries:
            return queries
        terms = [t.strip() for t in topic.split(",") if t.strip()]
        if not terms:
            terms = [topic]
        return terms

    def _search(self, query: str, since: str, limit: int) -> list[Post]:
        """Search Bluesky posts via the public API."""
        limit = min(limit, 100)
        params = urlencode({
            "q": query,
            "limit": limit,
            "since": since,
            "sort": "latest",
        })
        url = f"https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?{params}"
        data = _bsky_get(url)
        return self._normalize(data)

    def _normalize(self, data: dict) -> list[Post]:
        """Convert Bluesky API response into normalized Post objects."""
        posts = []
        for item in data.get("posts", []):
            # Author info
            author = item.get("author", {})
            handle = author.get("handle", "unknown")
            display_name = author.get("displayName", "")

            # Post text from record
            record = item.get("record", {})
            text = record.get("text", "")
            created_at = record.get("createdAt", "")

            # Build URL: at://did/app.bsky.feed.post/rkey → https://bsky.app/profile/handle/post/rkey
            uri = item.get("uri", "")
            rkey = uri.rsplit("/", 1)[-1] if uri else ""
            url = f"https://bsky.app/profile/{handle}/post/{rkey}" if rkey else ""

            # Engagement metrics
            like_count = item.get("likeCount", 0)
            repost_count = item.get("repostCount", 0)
            reply_count = item.get("replyCount", 0)

            posts.append(Post(
                source="bluesky",
                author=f"@{handle}",
                text=text,
                url=url,
                timestamp=created_at,
                score=like_count + repost_count,
                metadata={
                    "display_name": display_name,
                    "likes": like_count,
                    "reposts": repost_count,
                    "replies": reply_count,
                    "langs": record.get("langs", []),
                },
            ))

        return posts
