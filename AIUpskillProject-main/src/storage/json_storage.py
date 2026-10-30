"""Save articles as JSON (swap-in ArticleStorage implementation)."""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from src.models.article import Article
from src.storage.base_storage import ArticleStorage


class JSONStorage(ArticleStorage):
    """JSON implementation of ArticleStorage."""

    def __init__(self, base_path: str = "data/articles_json"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, articles: List[Article], filename: Optional[str] = None) -> Path:
        if filename is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = f"articles_{timestamp}.json"
        elif not filename.endswith(".json"):
            filename = f"{Path(filename).stem}.json"

        filepath = self.base_path / filename
        payload = [_convert_to_dict(article) for article in articles]
        filepath.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"Saved {len(articles)} articles to: {filepath}")
        return filepath


def _convert_to_dict(article: Article) -> dict:
    return {
        "title": article.title,
        "url": article.url,
        "published_at": article.published_at.isoformat(),
        "source": article.source,
        "summary": article.summary,
        "score": article.score,
    }
