"""Fetch top stories from HackerNews."""

import asyncio
from typing import Dict, List, Optional

import aiohttp

from src.models.article import Article
from src.fetchers.base_fetcher import BaseFetcher
from src.storage.base_storage import ArticleStorage
from src.transformers.article_transformer import ArticleTransformer
from src.strategies.rate_limit_strategy import RateLimitStrategy, SemaphoreStrategy
import logging

logger = logging.getLogger(__name__)

class HackerNewsFetcher(BaseFetcher):
    """
    Fetches top stories from HackerNews API.

    API Docs: https://github.com/HackerNews/API
    """

    BASE_URL = "https://hacker-news.firebaseio.com/v0"

    def __init__(self,transformer: Optional[ArticleTransformer] = None,
        storage: Optional[ArticleStorage] = None,
        limit: int = 30,rate_limiter=None):

        super().__init__(transformer, storage)
        self.limit = limit
        self.rate_limiter = rate_limiter or SemaphoreStrategy(10)
        # super().__init__(transformer,storage,rate_limiter, source_name="hackernews")
        # self.limit=limit

    async def fetch_articles(self) -> List[Article]:
        """Fetch from HackerNews API."""
        print(f"📰 Fetching {self.limit} stories from HackerNews...")
        try:

            story_ids = await self._fetch_top_story_ids()
            items = await asyncio.gather(*(self._fetch_story(i) for i in story_ids[: self.limit]))
            articles = self.transformer.transform_hackernews(items)
            print(f"Fetched {len(articles)} HackerNews stories")
            return articles
        except Exception as e:
                    logger.error(f"Fetch failed: {e}")
                    return []

    
    def get_source_name(self) -> str:
        """Return source name."""
        return "hackernews"

    async def fetch(self,limit: Optional[int] = None) -> List[Article]:
        """
        Fetch top stories from HackerNews.

        Args:
            limit: Number of stories to fetch (default 30)

        Returns:
            List of Article objects
        """
        if limit is not None:
            self.limit = limit

        print(f"📰 Fetching {limit or self.limit} stories from HackerNews...")
        return await self.fetch_articles()


    async def fetch_and_save(self, limit: int = 30) -> List[Article]:
        """Fetch articles and save to markdown."""
        articles = await self.fetch_articles()

        if articles:
            self.storage.save(articles, "hackernews_articles.md")

        return articles

    async def _fetch_top_story_ids(self) -> List[int]:
        """Fetch list of top story IDs."""
        url = f"{self.BASE_URL}/topstories.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                story_ids = await response.json()
                return story_ids

    async def _fetch_stories(self, story_ids: List[int]) -> List[Article]:
        """
        Fetch multiple stories concurrently.

        This is where async shines - fetch all at once!
        """
        # Create tasks for all stories
        tasks = [self._fetch_story(story_id) for story_id in story_ids]

        # Run all tasks concurrently
        stories = await asyncio.gather(*tasks)

        # Filter out None (failed fetches)
        return [s for s in stories if s is not None]

    async def _fetch_story(self, story_id: int) -> Article:
        """Fetch single story by ID."""
        url = f"{self.BASE_URL}/item/{story_id}.json"

        try:
            # Use rate limiter
            async with self.rate_limiter:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        return await response.json()

        except Exception as e:
            print(f"⚠️  Failed to fetch story {story_id}: {e}")
            return None


# Test it
async def test_fetch():
    """Quick test of fetcher."""
    fetcher = HackerNewsFetcher()
    articles = await fetcher.fetch(limit=5)

    print(f"\n📊 Results:")
    for article in articles:
        print(f"  - {article.title[:50]}...")

    return articles


if __name__ == "__main__":
    asyncio.run(test_fetch())
