# Smart Library - Architecture Documentation

## Complete System Flow:

```
┌───────────────────┐     ┌─────────────────────┐     ┌───────────────────────┐
│  Voice Input      │────>│   Model Runner      │────>│     Search Engine      │
│  (Recording)      │     │   (Whisper STT +    │     │                       │
└───────────────────┘     │    NLU LLM)         │     │  Open Library,        │
                          └─────────────────────┘     │  Project Gutenberg,   │
                                                     │  Internet Archive      │
                                                     └──────────┬──────────────┘
                                                               │
                                                    ┌──────────▼──────────────┐
                                                    │ PDF Compiler           │
                                                    │ (Content Extractor +    │
                                                    │ Chapter Splitter)      │
                                                    └──────────┬──────────────┘
                                                               │
                                                    ┌──────────▼──────────────┐
                                                    │ Full Book PDF Generator │
                                                    │ (TOC + Metadata +       │
                                                    │ Easy Navigation)        │
                                                    └─────────────────────────┘
```

## Component Diagram:

### Voice Input Module (`src/voice/`)
- **`recorder.py`** - Microphone access, audio capture, timer, waveform
  - `VoiceRecorder` class - Main recording with sounddevice
  - `WhisperSTTEngine` class - Audio transcription (multilingual support)
  - `WaveformVisualizer` class - Real-time energy bar display
- **`language_manager.py`** - Multilingual support (8 languages)
  - `LanguageSelector` - First launch dialog + settings integration

### Model Runner Module (`src/models/`)
- **`model_runner.py`** - Orchestrates STT + NLU models locally
- **`nlu_parser.py`** - Extracts book info from transcripts

### Search Module (`src/search/`)
- **`unified_search.py`** - Aggregates results from all sources
- **`open_library_client.py`** - Open Library API integration
- **`gutenberg_client.py`** - Project Gutenberg public domain books
- **`archive_client.py`** - Internet Archive digital copies

### PDF Compiler Module (`src/pdf_compiler/`)
- **`compiler.py`** - Full book content extraction
  - `ContentExtractor` - Scrapes HTML from book sources
  - `ContentFormatter` - Formats content for PDF
  - `TOCGenerator` - Creates table of contents
- **`metadata.py`** - Embeds book metadata (author, ISBN, source)

### Configuration (`config/`)
- **`settings.yaml`** - All app settings + language configuration
- **`defaults.yaml`** - Default values for optional features
