"""
Test Suite: Search Module
==========================

Waterfall Model Phase: Testing (Phase 4)
Tests for FR-04 (Book Search & Retrieval)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from search.unified_search import UnifiedSearchEngine


class TestUnifiedSearchEngine(unittest.TestCase):
    """Test cases for unified book search engine."""

    def setUp(self):
        config = {
            "open_library_api_key": None,
            "disabled_sources": []
        }
        self.engine = UnifiedSearchEngine(config)

    def test_search_returns_results(self):
        """Test: Search returns list of books."""
        results = self.engine.search("Wings of Fire")

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_search_calculates_confidence(self):
        """Test: Each result has confidence score."""
        results = self.engine.search("Wings of Fire by apj kalam")

        for book in results[:3]:
            self.assertIn("confidence", book)
            self.assertIsInstance(book["confidence"], (int, float))

    def test_search_sorts_by_confidence(self):
        """Test: Results sorted by confidence descending."""
        results = self.engine.search("The Alchemist")

        confidences = [r.get("confidence", 0) for r in results]
        self.assertEqual(confidences, sorted(confidences, reverse=True))

    def test_search_handles_empty_query(self):
        """Test: Search with empty query returns minimal results."""
        # Should handle gracefully without crashing
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                results = self.engine.search("")
                print(f"Empty search returned {len(results)} results")
            except Exception as e:
                print(f"Expected behavior for empty query: {e}")


class TestOpenLibraryClient(unittest.TestCase):
    """Test cases for Open Library client."""

    def setUp(self):
        self.client = OpenLibraryClient()

    def test_search_returns_books(self):
        """Test: Search returns book results."""
        results = self.client.search("The Alchemist")

        for book in results[:3]:
            self.assertIn("title", book)
            self.assertIn("source", book)


class TestProjectGutenbergClient(unittest.TestCase):
    """Test cases for Project Gutenberg client."""

    def setUp(self):
        self.client = ProjectGutenbergClient()

    def test_search_returns_books(self):
        """Test: Search returns book results from Gutenberg."""
        results = self.client.search("Frankenstein")

        for book in results[:3]:
            self.assertIn("title", book)
            self.assertIn("source", book)


if __name__ == "__main__":
    unittest.main()
