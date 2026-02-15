from .base import Post, SourceAdapter
from .x import XAdapter
from .reddit import RedditAdapter
from .civitai import CivitAIAdapter
from .arxiv import ArxivAdapter
from .lobsters import LobstersAdapter
from .bluesky import BlueskyAdapter

ADAPTERS = {
    "x": XAdapter,
    "reddit": RedditAdapter,
    "civitai": CivitAIAdapter,
    "arxiv": ArxivAdapter,
    "lobsters": LobstersAdapter,
    "bluesky": BlueskyAdapter,
    "bsky": BlueskyAdapter,
}

__all__ = ["Post", "SourceAdapter", "XAdapter", "RedditAdapter", "CivitAIAdapter", "ArxivAdapter", "LobstersAdapter", "BlueskyAdapter", "ADAPTERS"]
