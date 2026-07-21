# Smart Library - Version History

## v0.2.3 - Waveform & Timer Display 🟢 IN DEVELOPMENT
**Release Date:** 2026-07-21  
**Current Milestone:** PHASE 3 - Sprint 1 Tasks 1.3 & 1.4 Complete

### New Features:
- ✅ **Countdown Timer Display** - Shows remaining time (9s, 8s, 7s...) during recording
- ✅ **Waveform Visualization** - Real-time audio energy bar display
- ✅ **Waveform Visualizer Class** - Separate component for UI integration
- ✅ **Enhanced Error Handling** - Better exception handling in all modules

### Changed:
- `src/voice/recorder.py` - Added timer thread, waveform visualization methods
  - New `_start_timer()` method for countdown display
  - New `get_waveform()` method for energy calculation
  - Enhanced `stop_recording()` with numpy array handling
  - Added WaveformVisualizer class for UI components
- `test_recorder.py` - Updated with visual feedback tests

### Technical Changes:
- Non-blocking timer thread for responsive UI
- Waveform energy normalization (0-1 range)
- Audio data stored as numpy float arrays
- Error handling improvements with traceback logging

### Git Commits (Latest):
```
commit 3d081c4...
    PHASE 3 - Sprint 1 Tasks 1.3 & 1.4: Waveform Display + Whisper STT

commit 2a8e1ce...
    PHASE 3 - Sprint 1 Task 1.2: Audio Capture Implementation Complete

commit a381093...
    PHASE 3 - Sprint 1 Task 1.1: Microphone Access Setup
```

---

## v0.2.2 - Implementation Phase Started 🟡 IN DEVELOPMENT
**Release Date:** 2026-07-21  

### New Features:
- ✅ **Phase 3 Implementation** - Production code development started
- ✅ **Real Microphone Access** - sounddevice integration for live audio capture
- ✅ **Waveform Support** - Ready for real-time visualization (T-1.3)

### Changed:
- `src/voice/recorder.py` - Completely rewritten with production audio capture
  - Added real microphone access via sounddevice
  - Implemented non-blocking recording thread
  - Proper WAV file saving with metadata
  - Audio normalization to prevent clipping
- `requirements.txt` - Added audio processing dependencies
- `AGILE_TRACKER.md` - Sprint 1 updated with implementation progress

---

## v0.2.1 - Multilingual Support Added 🌍 STABLE
**Release Date:** 2026-07-20

### New Features:
- ✅ **Multilingual Voice Input** - 8 Indian languages supported:
  - English, Hindi (हिन्दी), Telugu (తెలుగు), Tamil (தமிழ்)
  - Bengali (বাংলা), Marathi (मराठी), Kannada (ಕನ್ನಡ), Gujarati (ગુજરાતી)
- ✅ **Language Selection Dialog** - Shown on first app launch
- ✅ **Settings Integration** - Language can be changed in Settings tab

### Files Changed:
- `src/voice/language_manager.py` - NEW - Multilingual support manager
- `src/voice/recorder.py` - Updated with language parameter
- `config/settings.yaml` - Added language configuration section
- `AGILE_TRACKER.md` - Sprint 1 updated with multilingual completion

---

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

---

## Git Repository

**URL:** https://github.com/Aumnamaha/Smart_Library  
**Branch:** main  
**Total Commits:** 11 commits pushed

**Latest Changes:** 
- PHASE 3 Implementation started
- Sprint 1 Tasks 1.1-1.4 complete (microphone, capture, timer, waveform)
- Ready for Whisper large model download and transcription testing

