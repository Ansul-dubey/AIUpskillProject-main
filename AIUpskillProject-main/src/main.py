"""Main entry point for news fetcher."""

import asyncio
import sys

from src.orchestrator import FetchOrchestrator
from src.storage.markdown_storage import MarkdownStorage
from src.transformers.article_transformer import ArticleTransformer
from src.fetchers.hackernews_fetcher import HackerNewsFetcher
from src.fetchers.github_trending_fetcher import GitHubTrendingFetcher

async def main():
    """Main function."""
    print("=" * 60)
    print("  AI Agent Onboarding - News Fetcher")
    print("  Milestone 1: Async News Fetcher")
    print("=" * 60)

    try:
        """Main entry point with dependency injection."""
        
        # Create dependencies
        transformer = ArticleTransformer()
        storage = MarkdownStorage("data/articles")
        
        # Create fetchers
        fetchers = [
            HackerNewsFetcher(transformer, storage),
            GitHubTrendingFetcher(transformer, storage),
        ]
        
        # Inject dependencies into orchestrator
        orchestrator = FetchOrchestrator(
            fetchers=fetchers,
            storage=storage,
            transformer=transformer
        )
        
        # Run
        articles = await orchestrator.fetch_all()
        print(f"✅ Fetched {len(articles)} articles total")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())