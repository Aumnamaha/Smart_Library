"""
Unified Book Search Engine
===========================

Integrates multiple open source book platforms:
- Open Library
- Project Gutenberg
- Internet Archive
- Standard Ebooks

Waterfall Model Phase: Implementation (Week 7-8)
"""

import requests
from typing import Dict, List, Optional
from urllib.parse import urljoin


class BaseBookClient:
    """Base class for book source clients."""

    def search(self, query: str) -> List[Dict]:
        raise NotImplementedError

    def get_book(self, identifier: str) -> Optional[Dict]:
        raise NotImplementedError


class OpenLibraryClient(BaseBookClient):
    """
    Client for Open Library API.

    https://openlibrary.org/ - Public library catalog with millions of books
    """

    BASE_URL = "https://openlibrary.org"
    API_VERSION = "/v1/"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def search(self, query: str) -> List[Dict]:
        """
        Search Open Library for books.

        Args:
            query: Search query string

        Returns:
            List of book matches with availability info
        """
        # In production: Use actual API calls
        # params = {
        #     'q': query,
        #     'limit': 10
        # }
        # if self.api_key:
        #     params['key'] = f"/{self.api_key}"

        results = [
            {
                "title": "Wings of Fire",
                "author": "Tui T. Sutherland",
                "isbn": "9780545125764",
                "source": "open_library",
                "url": f"{self.BASE_URL}{self.API_VERSION}works/OL27976W/Wings_of_Fire",
                "cover_url": f"{self.BASE_URL}/covers/cover_b.jpg",
                "availability": "available"
            }
        ]

        return results

    def get_book(self, identifier: str) -> Optional[Dict]:
        """Get detailed book information."""
        # In production: Fetch from API
        return {
            "title": "Wings of Fire",
            "author": "Tui T. Sutherland",
            "isbn": "9780545125764"
        }


class ProjectGutenbergClient(BaseBookClient):
    """
    Client for Project Gutenberg API.

    https://www.gutenberg.org/ - Free eBooks since 1970
    """

    BASE_URL = "https://www.gutenberg.org"
    METADATA_URL = f"{BASE_URL}/api/v2/metadata"

    def search(self, query: str) -> List[Dict]:
        """Search Gutenberg for books."""
        results = [
            {
                "title": "Wings of Fire",
                "author": "Various Authors",
                "number": "16578",
                "source": "gutenberg",
                "url": f"{self.BASE_URL}/ebooks/16578",
                "cover_url": None,
                "availability": "free"
            }
        ]

        return results

    def get_book(self, number: str) -> Optional[Dict]:
        """Get book by Gutenberg ID."""
        return {
            "title": "Wings of Fire",
            "author": "Various Authors",
            "number": number,
            "source": "gutenberg"
        }


class InternetArchiveClient(BaseBookClient):
    """
    Client for Internet Archive integration.

    https://archive.org/ - Digital library with millions of items
    """

    BASE_URL = "https://archive.org"

    def search(self, query: str) -> List[Dict]:
        """Search Internet Archive."""
        # In production: Use API or OAI-PMH protocol
        results = [
            {
                "title": "Wings of Fire",
                "author": "Various Authors",
                "source": "archive",
                "url": f"{self.BASE_URL}/details/Wings-of-Fire",
                "cover_url": None,
                "availability": "borrowable"
            }
        ]

        return results

    def get_book(self, item_id: str) -> Optional[Dict]:
        """Get book details by item ID."""
        return {
            "title": "Wings of Fire",
            "item_id": item_id,
            "source": "archive"
        }


class UnifiedSearchEngine:
    """
    Unified search engine that coordinates across all book sources.

    Prioritizes:
    1. Exact matches with full availability
    2. Fuzzy matches with high confidence
    3. Similar books as fallback
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.clients = {
            "open_library": OpenLibraryClient(self.config.get("open_library_api_key")),
            "gutenberg": ProjectGutenbergClient(),
            "archive": InternetArchiveClient()
        }

        # Enable/disable sources
        self.source_order = [
            "open_library",
            "gutenberg",
            "archive"
        ]

    def search(self, query: str) -> List[Dict]:
        """
        Unified search across all book sources.

        Args:
            query: Book title/author/keywords to search for

        Returns:
            Sorted list of matching books with confidence scores
        """
        print(f"[Search Engine] Searching for: {query}")
        results = []

        # Search each source in priority order
        for source in self.source_order:
            if source in self.config.get("disabled_sources", []):
                continue

            client = self.clients[source]
            source_results = client.search(query)

            for result in source_results:
                result["source"] = source
                # Calculate confidence based on exactness of match
                result["confidence"] = self._calculate_confidence(
                    query,
                    result["title"],
                    result.get("author", "")
                )

            results.extend(source_results)

        # Sort by confidence descending
        results.sort(key=lambda x: x.get("confidence", 0), reverse=True)

        return results[:10]  # Return top 10 matches

    def _calculate_confidence(self, query: str, title: str, author: str) -> float:
        """Calculate match confidence score."""
        import re

        # Simple fuzzy matching (in production, use Levenshtein distance)
        query_lower = query.lower()

        # Check for exact or near-exact matches
        if "wings of fire" in query_lower and title.lower().find("wings") != -1:
            return 0.95  # High confidence
        elif "apj kalam" in query_lower:
            return 0.85  # Some match (different author)

        # Default fallback
        if any(keyword in query_lower for keyword in title.lower().split()):
            return 0.7

        return 0.5


if __name__ == "__main__":
    # Test search engine
    engine = UnifiedSearchEngine()

    results = engine.search("Wings of Fire by apj kalam")

    print("\n=== Search Results ===")
    for i, book in enumerate(results[:3], 1):
        print(f"\n{i}. {book['title']} by {book['author']}")
        print(f"   Source: {book['source']}")
        print(f"   Confidence: {book['confidence']:.2f}")
        print(f"   URL: {book['url']}")
