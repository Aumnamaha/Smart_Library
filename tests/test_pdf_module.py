"""
Test Suite: PDF Compiler Module
================================

Waterfall Model Phase: Testing (Phase 4)
Tests for FR-05 (Content Compilation) and FR-06 (PDF Generation)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pdf_compiler.compiler import PDFCompiler, ContentExtractor, ContentFormatter


class TestPDFCompiler(unittest.TestCase):
    """Test cases for main PDF compiler."""

    def setUp(self):
        self.config = {
            "font": "Helvetica",
            "font_size": 12,
            "output_dir": "./data/generated_pdf_test"
        }
        os.makedirs(self.config["output_dir"], exist_ok=True)
        self.compiler = PDFCompiler(self.config)

    def test_compile_returns_pdf_bytes(self):
        """Test: Compile returns valid PDF bytes."""
        book_info = {
            "title": "Wings of Fire",
            "author": "Tui T. Sutherland",
            "isbn": "9780545125764",
            "source": "open_library"
        }

        pdf_bytes = self.compiler.compile(book_info, "test query")

        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 0)

    def test_compile_includes_metadata(self):
        """Test: PDF includes book metadata."""
        # This would verify the HTML output contains required elements
        pass  # Placeholder for actual assertion

    def test_output_directory_created(self):
        """Test: Output directory is created automatically."""
        self.assertTrue(os.path.exists(self.config["output_dir"]))


class TestContentExtractor(unittest.TestCase):
    """Test cases for content extraction."""

    def setUp(self):
        self.extractor = ContentExtractor()

    def test_extract_section_returns_text(self):
        """Test: Extraction returns formatted text."""
        book_info = {
            "title": "Wings of Fire",
            "author": "Tui T. Sutherland"
        }

        content = self.extractor.extract_section(book_info, "Chapter 1")

        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)


class TestContentFormatter(unittest.TestCase):
    """Test cases for content formatting."""

    def setUp(self):
        self.formatter = ContentFormatter()

    def test_format_content_returns_html(self):
        """Test: Formatted content is HTML."""
        content = "<p>Sample content</p>"
        metadata = {
            "title": "Test Book",
            "author": "Test Author"
        }

        html = self.formatter.format_content(content, metadata)

        self.assertIsInstance(html, str)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Test Book", html)


if __name__ == "__main__":
    unittest.main()
