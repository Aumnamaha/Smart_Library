# 📚 Smart Library — Voice-Powered Book Discovery

> **AI-powered library system using local voice transcription and LLM-based search to find and compile complete book PDFs from open-source platforms.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

---

## 📋 Executive Summary

**Smart Library** is a voice-enabled intelligent library system that understands natural language book queries through local AI models and provides complete book downloads from open-source platforms. Built following the Waterfall SDLC model, it supports **8 Indian languages** plus English for inclusive access.

> ⚠️ **Status:** Project in active development — Implementation phase (Phase 3 of 6). Core architecture documented; full setup instructions pending completion of source code modules.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🎙️ **Voice-to-Text** | Local speech transcription using Whisper or equivalent STT model |
| 🔍 **AI Book Search** | Natural language queries to find books across open-source platforms |
| 📥 **Full PDF Generation** | Complete book downloads (not excerpts) from Open Library, Project Gutenberg, Internet Archive |
| 🌍 **Multilingual Support** | English, Hindi, Telugu, Tamil, Bengali, Marathi, Kannada, Gujarati |
| 🤖 **Local AI Models** | All processing runs offline — no external API dependencies |

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌───────────────────┐
│  Voice Input    │────>│  Model Runner   │────>│    Search Engine  │
│  (Recording)    │     │  (Whisper/      │     │                   │
│                 │     │   local LLM)    │     │ Open Library,     │
└─────────────────┘     └─────────────────┘     │ Project Gutenberg │
                                                └───────────┬───────┘
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

## 📊 Development Status — Waterfall Model

| Phase | Status | Deliverables |
|---|---|---|
| **1. Requirements** | ✅ Complete | SRS, User Stories, Use Cases |
| **2. System Design** | ✅ Complete | Architecture, DB Schema, API Specs |
| **3. Implementation** | 🔄 In Progress | Source code modules (voice/, models/, search/, pdf_compiler/) |
| **4. Testing** | ⏳ Pending | Test plans, test cases |
| **5. Deployment** | ⏳ Pending | Production build |
| **6. Maintenance** | ⏳ Pending | Update logs |

---

## 🚀 Quick Start (Preview)

### Prerequisites

- **Python 3.10+** installed on your system
- **Node.js 18+** (for frontend components, if applicable)

### Installation (Pending Implementation Completion)

```powershell
# Step 1: Clone the repository
git clone https://github.com/Aumnamaha/Smart_Library.git
cd Smart_Library

# Step 2: Activate virtual environment
& "C:\Users\Aum Namaha\Documents\finalenv\Scripts\Activate.ps1"

# Step 3: Install dependencies (once requirements.txt is finalized)
# pip install -r requirements.txt

# Step 4: Launch the application
# python app.py   # or: streamlit run app.py
```

Detailed setup instructions are available in [`INSTALL.md`](<INSTALL.md>) once implementation is complete.

---

## 📁 Project Structure (Planned)

```
Smart_Library/
├── README.md                 # This file
├── INSTALL.md                # Setup instructions (pending)
├── PLANNING.md               # Waterfall planning documents
├── requirements.txt          # TBD — to be finalized with implementation
├── src/                      # Source code modules
│   ├── voice/                # Voice recording & transcription
│   ├── models/               # AI model management (Whisper, LLM)
│   ├── search/               # Book search across open-source platforms
│   └── pdf_compiler/         # PDF generation logic
├── docs/                     # Documentation
├── tests/                    # Test files
├── config/                   # Configuration files
└── data/                     # Model downloads & cache
```

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| **STT** | Whisper (local) or equivalent local model |
| **LLM** | Llama-3-8B / Mistral / Phi-3 (local inference) |
| **Backend** | Python with FastAPI/Flask |
| **PDF Generation** | WeasyPrint / PyPDF2 / pdfkit |
| **Book Sources** | Open Library, Project Gutenberg, Internet Archive |

---

## 👤 Author

**Maintained by [Thirunagari Aum Namaha](https://github.com/Aumnamaha)** • [LinkedIn](https://www.linkedin.com/in/aumnamaha-thirunagari-9214782bb/)

---

## 📜 License

This project uses only open-source libraries and platforms. Licensed under MIT.
