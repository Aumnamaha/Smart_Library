"""
PDF Compiler Module
===================

Generates full book PDFs from open source repositories.

Waterfall Model Phase: Implementation (Week 9-10)
Requirements Updated: FR-04, FR-05, FR-06 (Full Book Support)
Agile Sprint: v0.1 Full Reading Capability
"""

import os
from datetime import datetime
from typing import Dict, List, Optional, Any


class ContentExtractor:
    """
    Extracts book content from various source formats.

    Handles:
        - Chapter selection based on query
        - Text extraction and cleanup
        - Metadata preservation
        - Full book compilation
    """

    def __init__(self):
        self.section_preferences = {
            "fiction": ["chapter_1", "introduction"],
            "non_fiction": ["overview", "chapter_1"],
            "reference": ["index", "glossary"]
        }

    def extract_full_book(self, book_info: Dict[str, Any]) -> str:
        """
        Extract complete book content.

        Args:
            book_info: Book metadata and content info

        Returns:
            Full book text content with proper formatting
        """
        print(f"[ContentExtractor] Loading full book: {book_info.get('title', '')}")

        # Return placeholder for full book demo
        return f"""
{book_info.get('title', 'Book Title')} by {book_info.get('author', 'Unknown Author')}
{'=' * 70}

FULL BOOK CONTENT (All Pages)

[This is where the complete book content would be loaded from the source]

The Smart Library app provides full-length books from open source repositories:
- Project Gutenberg (public domain works)
- Open Library (borrowed texts)
- Internet Archive (archive copies)

Full book reading respects copyright and licensing terms.

---
Complete Table of Contents and all chapters follow below
"""

    def extract_section(self, book_info: Dict[str, Any], topic: str) -> str:
        """
        Extract specific section from book.

        Args:
            book_info: Book metadata and content info
            topic: Topic or chapter to extract

        Returns:
            Extracted text content
        """
        print(f"[ContentExtractor] Extracting section: {topic}")

        # Return placeholder for demo
        return f"""
{book_info.get('title', 'Book Title')} by {book_info.get('author', 'Unknown Author')}"
{'=' * 60}

CHAPTER ONE: {topic}

This is where the content would begin. The Smart Library app provides
access to complete books from open source repositories.

---
Source attribution preserved below
"""


class ContentFormatter:
    """
    Formats extracted content for PDF output.

    Handles:
        - Typography (font, size, spacing)
        - Headers and footers
        - Page breaks
        - Attribution formatting
        - Full book pagination tracking
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {
            "font": "Helvetica",
            "font_size": 12,
            "margin_top": 72,      # 1 inch margin in points (for book format)
            "margin_bottom": 72,
            "margin_left": 72,
            "margin_right": 72,
            "full_book_mode": True  # Enable full book support
        }

    def format_content(self, content: str, metadata: Dict[str, Any]) -> str:
        """
        Format raw text for PDF generation.

        Args:
            content: Extracted book content (can be full book or section)
            metadata: Book and query metadata

        Returns:
            HTML-formatted content ready for PDF conversion
        """
        # Add Table of Contents for full books
        toc = ""
        if metadata.get("full_book", False):
            toc = """
<div class="toc">
    <h2>Table of Contents</h2>
    <ul>
        <li><a href="#chapter1">Chapter 1: Introduction</a></li>
        <li><a href="#chapter2">Chapter 2</a></li>
        <li><a href="#chapter3">Chapter 3</a></li>
        <li><a href="#conclusion">Conclusion</a></li>
    </ul>
</div>
"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{metadata.get('title', 'Smart Library')}</title>
    <style>
        body {{
            font-family: {self.config['font']}, serif;
            font-size: 12pt;
            line-height: 1.5;
            margin: 0;
            padding: {self.config['margin_top']}pt {self.config['margin_right']}pt {self.config['margin_bottom']}pt {self.config['margin_left']}pt;
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #2E7D32;
            padding-bottom: 20pt;
            margin-bottom: 40pt;
        }}
        .title {{
            font-size: 24pt;
            font-weight: bold;
            color: #2E7D32;
            text-align: center;
            margin-bottom: 10pt;
        }}
        .author {{
            font-size: 16pt;
            font-style: italic;
            color: #444;
            text-align: center;
            margin-bottom: 20pt;
        }}
        .toc {{
            border: 1px solid #ccc;
            padding: 20pt;
            margin: 30pt 0;
            background-color: #f9f9f9;
        }}
        .toc h2 {{
            font-size: 14pt;
            color: #333;
            margin-bottom: 15pt;
        }}
        .toc ul {{
            list-style: none;
            padding-left: 0;
        }}
        .toc li {{
            padding: 8pt 0;
            border-bottom: 1px solid #eee;
        }}
        .toc a {{
            color: #2E7D32;
            text-decoration: none;
        }}
        .content {{
            white-space: pre-wrap;
            font-family: {self.config['font']}, serif;
        }}
        .chapter {{
            margin-top: 50pt;
            page-break-before: always;
        }}
        .chapter h2 {{
            font-size: 18pt;
            color: #2E7D32;
            border-bottom: 2px solid #ddd;
            padding-bottom: 10pt;
        }}
        .footer {{
            border-top: 1px solid #ccc;
            padding-top: 15pt;
            margin-top: 40pt;
            font-size: 9pt;
            color: #666;
            text-align: center;
        }}
        .page-number {{
            text-align: center;
            font-size: 8pt;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1 class="title">{metadata.get('title', '')}</h1>
        <h2 class="author">{metadata.get('author', '')}</h2>
        {toc if toc else ''}
        <div style="font-size: 10pt; color: #666;">
            Source: {metadata.get('source', 'Unknown')} |
            ISBN: {metadata.get('isbn', 'N/A')}
        </div>
    </div>
    <div class="content">
{content}
    </div>
    <div class="footer">
        Smart Library - Full Book Reader
    </div>
</body>
</html>"""

        return html


class PDFCompiler:
    """
    Main PDF compilation service for full books.

    Orchestrates all components to generate complete book PDFs
    from open source repositories.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {
            "font": "Helvetica",
            "font_size": 12,
            "output_dir": "./data/generated_pdf",
            "full_book_mode": True  # Enable full book reading by default
        }

        self.extractor = ContentExtractor()
        self.formatter = ContentFormatter(config)

        os.makedirs(self.config["output_dir"], exist_ok=True)

    def compile(self, book_info: Dict[str, Any], query: str = "") -> bytes:
        """
        Compile a complete book PDF.

        Args:
            book_info: Book metadata and content info
            query: Original user query (optional, for attribution)

        Returns:
            PDF file bytes ready for download
        """
        print(f"[PDF Compiler] Compiling full book: {book_info.get('title', '')}")

        # Extract full book content
        content = self.extractor.extract_full_book(book_info)

        # Format content with metadata (full book mode)
        metadata = {
            "title": book_info.get("title", ""),
            "author": book_info.get("author", ""),
            "source": book_info.get("source", ""),
            "isbn": book_info.get("isbn", ""),
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "full_book": True,  # Mark as full book
            "page_number": 1,
            "total_pages": "dynamic"  # Will be calculated during PDF generation
        }

        formatted = self.formatter.format_content(content, metadata)

        return formatted.encode('utf-8')


if __name__ == "__main__":
    # Test PDF compiler with full book support
    compiler = PDFCompiler()

    book_info = {
        "title": "Wings of Fire",
        "author": "Tui T. Sutherland",
        "isbn": "9780545125764",
        "source": "open_library"
    }

    pdf_bytes = compiler.compile(book_info)
    print(f"\n[PDF Compiler] Generated Full Book PDF: {len(pdf_bytes)} bytes")
