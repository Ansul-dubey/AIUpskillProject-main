"""Main entry point for news fetcher."""

import asyncio
import sys

from src.factories.fetcher_factory import FetcherFactory
from src.orchestrator import FetchOrchestrator
from src.storage.markdown_storage import MarkdownStorage
from src.strategies.rate_limit_strategy import SemaphoreStrategy
from src.transformers.article_transformer import ArticleTransformer


def build_orchestrator() -> FetchOrchestrator:
    """Builds default dependencies. Creates FeetchOrchestrator Object"""
    transformer = ArticleTransformer()
    storage = MarkdownStorage("data/articles")
    fetchers = [
        FetcherFactory.create(
            "hackernews",
            transformer,
            storage,
            rate_limiter=SemaphoreStrategy(10),
        ),
        FetcherFactory.create(
            "rss",
            transformer,
            storage,
            feed_url="https://hnrss.org/frontpage",
        ),
        FetcherFactory.create(
            "github",
            transformer,
            storage,
        ),
    ]
    return FetchOrchestrator(
        fetchers=fetchers,
        storage=storage,
        transformer=transformer,
    )


async def main() -> int:
    """Main function."""
    print("=" * 60)
    print("  AI Agent Onboarding - News Fetcher")
    print("  Milestone 1: Async News Fetcher")
    print("=" * 60)

    try:
        """Main entry point with dependency injection."""
        orchestrator = build_orchestrator()
        articles = await orchestrator.fetch_all()
        print(f"✅ Fetched {len(articles)} articles total")
        print("Saved combined file to: data/articles/all_articles.md")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
