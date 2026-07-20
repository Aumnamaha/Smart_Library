# Smart Library App 📚

A voice-powered intelligent library system that uses local AI models to understand book queries and provide **complete book downloads**.

## Features

- **Voice-to-Text Transcription**: Record and transcribe user voice queries locally
- **AI Book Search**: Find books based on natural language queries
- **Smart Retrieval**: Locate full books from open source platforms
- **Full Book PDF Generation**: Download and read complete books, not just excerpts
- **Local AI Models**: All processing happens offline with local LLMs

---

## Table of Contents

- [Waterfall Model Phases](#waterfall-model-phases)
- [Quick Start](#quick-start)
- [Architecture Overview](#architecture-overview)
- [Technology Stack](#technology-stack)

---

## Waterfall Model Phases

This project follows the **Waterfall Software Development Model**:

```
Requirements → Design → Implementation → Testing → Deployment → Maintenance
           ↓             ↓              ↓          ↓            ↓
         SRS Doc    System Design   Code Base  Test Reports  Live App
                           Database UI     Unit Tests    Docs     Training
```

### Phase 1: Requirements Analysis ✅ (COMPLETED)

**Deliverables:** Software Requirements Specification (SRS), User Stories, Use Cases

**Key Requirements:**
- Voice recording and transcription functionality
- Natural language query processing
- Book search across open source platforms
- PDF content extraction and compilation
- Local AI model integration
- Offline-capable architecture

### Phase 2: System Design ✅ (COMPLETED)

**Deliverables:** System Architecture, Database Schema, API Specifications, UI Mockups

### Phase 3: Implementation 🔄

**Deliverables:** Source Code, Build Artifacts

### Phase 4: Testing ⏳

**Deliverables:** Test Plans, Test Cases, Bug Reports

### Phase 5: Deployment ⏳

**Deliverables:** Production Build, User Documentation

### Phase 6: Maintenance ⏳

**Deliverables:** Update Logs, Support Tickets

---

## Quick Start

See `INSTALL.md` for detailed setup instructions.

---

## Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Voice Input    │────>│  Model Runner   │────>│  Search Engine   │
│  (Recording)    │     │  (Whisper/      │     │                  │
└─────────────────┘     │   local LLM)    │     │  Open Library,   │
                        └─────────────────┘     │  Project Gutenberg│
                                                └────────────┬───────┘
                                                             │
                                                 ┌──────────▼──────────┐
                                                 │ PDF Compiler        │
                                                 │ (Summarizer +       │
                                                 │ Extractor)          │
                                                 └──────────┬──────────┘
                                                            │
                                                 ┌──────────▼──────────┐
                                                 │  PDF Generator      │
                                                 │   (Full Book PDF)   │
                                                 └─────────────────────┘
```

---

## Technology Stack

### AI/ML Models (Local)
- **Whisper** (or equivalent local STT): Voice-to-text transcription
- **LLM 1** (e.g., Llama-3-8B, Mistral): Natural language understanding & query parsing
- **LLM 2** (e.g., smaller model like Phi-3 or Gemma): Book search & retrieval

### Backend Framework
- **Python** with FastAPI/Flask for REST API
- Or **Node.js** with Express if preferred

### PDF Generation
- **WeasyPrint** or **PyPDF2** for Python
- Or **pdfkit** / **Puppeteer** for Node.js

### Open Source Book Sources
- [Open Library](https://openlibrary.org/)
- [Project Gutenberg](https://www.gutenberg.org/)
- [Internet Archive](https://archive.org/)
- [Z-Library Alternative](https://libgen.is)
- [Standard Ebooks](https://standardebooks.org/)

---

## Project Structure

```
Smart_Library/
├── README.md                 # This file
├── INSTALL.md                # Setup instructions
├── PLANNING.md               # Waterfall planning documents
├── src/                      # Source code
│   ├── voice/               # Voice recording & transcription
│   ├── models/              # AI model management
│   ├── search/              # Book search functionality
│   └── pdf_compiler/        # PDF generation logic
├── docs/                     # Documentation
├── tests/                    # Test files
├── config/                   # Configuration files
├── data/                     # Model downloads, cache
└── deploy/                   # Deployment scripts
```

---

## License

This project uses only open source libraries and platforms.
