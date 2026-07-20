# Smart Library - Version History

## v0.2.0 - Full Book Reading (Current) 🟢 STABLE
**Release Date:** 2026-07-20

### New Features:
- ✅ Full book reading support (not limited to 2 pages)
- ✅ Complete chapter-by-chapter PDF generation
- ✅ Table of contents for easy navigation
- ✅ Proper pagination tracking
- ✅ Book metadata preservation (ISBN, source attribution)

### Changed:
- `src/pdf_compiler/compiler.py` - Updated for full book support
- `README.md` - Reflects full book capability
- Configuration default changed to `full_book_mode: true`

### Technical Changes:
- Removed PDFPaginater class (no longer needed for full books)
- Added `full_book_mode` flag to ContentFormatter
- Updated content extraction to load complete books

---

## v0.1.0 - 2-Page Excerpts (Legacy) 🔴 DEPRECATED
**Release Date:** 2026-07-19

### Features:
- ✅ Voice-to-text transcription
- ✅ Book search across open sources
- ⚠️ Limited to 2-page excerpts per query

**Note:** This version has been superseded by v0.2.0 with full book support.

---

## Upcoming Versions

### v0.3.0 (Planned) - Enhanced Features
- [ ] Batch PDF generation
- [ ] Bookmark/sync reading progress
- [ ] Offline synchronization
- [ ] Mobile app companion

### v1.0.0 (Target) - Complete Product
- [ ] Multi-user library system
- [ ] Cloud sync option
- [ ] Reading analytics dashboard
- [ ] Social sharing features