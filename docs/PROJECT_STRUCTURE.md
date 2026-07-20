# Smart Library Project Structure

Complete file organization following Waterfall Model phases.

```
Smart_Library/
│
├── 📄 README.md                      # Project overview and quick start
├── 📄 INSTALL.md                     # Detailed installation guide
├── 📄 PLANNING.md                    # Waterfall model documentation
├── 📄 requirements.txt               # Python dependencies
│
├── 📁 src/                           # Source code
│   ├── __init__.py
│   ├── main.py                       # Application entry point (interactive mode)
│   ├── api/                          # REST API server
│   │   ├── __init__.py
│   │   └── server.py                 # FastAPI endpoints
│   │
│   ├── voice/                        # Voice recording & transcription
│   │   ├── __init__.py
│   │   └── recorder.py               # Audio recording, STT engine
│   │
│   ├── models/                       # AI model management
│   │   ├── __init__.py
│   │   └── model_runner.py           # Model loading & inference
│   │
│   ├── search/                       # Book search functionality
│   │   ├── __init__.py
│   │   └── unified_search.py         # Multi-source search engine
│   │
│   └── pdf_compiler/                 # PDF generation
│       ├── __init__.py
│       └── compiler.py               # Content extraction & formatting
│
├── 📁 data/                          # Data storage
│   ├── models/                       # Downloaded AI models
│   │   ├── whisper/                  # Speech-to-text models
│   │   └── microsoft/                # LLM models (Phi-3, etc.)
│   ├── audio/                        # Voice recordings
│   │   └── recordings/               # Temporary recording files
│   └── generated_pdf/                # Generated PDF excerpts
│
├── 📁 logs/                          # Application logs
│   └── app.log                       # Main application log file
│
├── 📁 tests/                         # Test suite
│   ├── __init__.py
│   ├── test_voice_module.py         # Voice module tests
│   ├── test_search_module.py        # Search module tests
│   └── test_pdf_module.py           # PDF compiler tests
│
├── 📁 config/                        # Configuration files
│   └── settings.yaml                 # Main configuration
│
├── 📁 docs/                          # Documentation
│   ├── API_DOCUMENTATION.md          # Complete API reference
│   ├── PROJECT_STRUCTURE.md         # This file
│   └── KNOWN_ISSUES.md              # Bug tracking
│
├── 📁 scripts/                       # Utility scripts
│   ├── setup.py                     # Installation automation
│   └── download_models.py           # Model download helper
│
└── 📄 .gitignore                     # Git ignore patterns
```

---

## Waterfall Phase Deliverables by Location

| Phase | Directory | Key Files |
|-------|-----------|-----------|
| **Requirements** | `PLANNING.md` (Phase 1 section) | SRS, User Stories, Use Cases |
| **Design** | `src/`, `config/`, `docs/` | Architecture diagrams, API specs, DB schema |
| **Implementation** | `src/**/*.py` | All source code modules |
| **Testing** | `tests/` | Unit and integration tests |
| **Deployment** | `install.py`, `docker-compose.yml` | Deployment scripts, configs |
| **Maintenance** | `logs/`, `.gitignore` | Monitoring, version control |

---

## File Descriptions

### Documentation Files

- **README.md**: Quick start overview, architecture summary
- **INSTALL.md**: Step-by-step installation instructions
- **PLANNING.md**: Waterfall model phases and planning documents

### Source Code (`src/`)

- **main.py**: Interactive CLI application
- **api/server.py**: REST API with FastAPI
- **voice/recorder.py**: Voice recording and STT handling
- **models/model_runner.py**: AI model management
- **search/unified_search.py**: Multi-source book search
- **pdf_compiler/compiler.py**: PDF generation logic

### Configuration (`config/`)

- **settings.yaml**: All application settings in one place

### Tests (`tests/`)

- Test files organized by module being tested
- Unit tests, integration tests, and system tests

---

## Git Ignore Rules

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
.Python
venv/
env/

# Data (can be downloaded separately)
data/models/*.pt
data/models/*.safetensors
data/generated_pdf/*
!.gitkeep

# Logs
logs/*.log

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Environment
.env
.env.local
```

---

## Deployment Artifacts

### Production Package Structure

```
Smart_Library_Producion_vX.Y.Z/
├── src/                    # Production source code
├── requirements.txt        # Production dependencies
├── config/                 # Production settings
└── models.tar.gz          # Pre-downloaded models
```

---

**Last Updated:** 2026-07-20  
**Project Status:** Phase 1 & 2 Complete, Implementing Phase 3
