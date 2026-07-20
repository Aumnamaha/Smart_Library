# Smart Library - Installation Guide

This guide will help you set up the Smart Library application on your system.

---

## Quick Start (5 Minutes)

### 1. System Requirements

**Hardware:**
- OS: Windows 10/11, Linux, or macOS
- RAM: Minimum 8GB (16GB recommended for better performance)
- Storage: Minimum 20GB free space
- Microphone: Required for voice input
- GPU: Optional (recommended for faster model inference)

**Software:**
- Python 3.10+ (for Python implementation) OR Node.js 18+ (for Node implementation)

---

## Method 1: Standalone Installation (Recommended)

### Step 1: Install Python Dependencies

Open a terminal and navigate to the project directory:

```bash
cd "C:\Users\a11au\OneDrive\Documents\Proj\Smart_Library"
```

Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:
```bash
pip install fastapi uvicorn python-multipart
pip install whisper torch  # Speech-to-text model
pip install transformers  # For local LLM
pip install openlibrary-client requests
pip install weasyprint pypdf2  # PDF generation
pip install pydantic email-validator
```

### Step 2: Download AI Models (First Time Only)

**Option A: Automatic Download (Recommended)**
```bash
python scripts/download_models.py --models whisper-tiny,phi-3-mini
```

**Option B: Manual Download**

Download these models to `data/models/`:

1. **Whisper Model** (Speech-to-Text)
   - URL: https://huggingface.co/openai/whisper-tiny
   - Size: ~76MB
   - Alternative: whisper-base (~309MB) for better accuracy

2. **LLM for Query Understanding**
   - Recommended: Microsoft Phi-3-mini (3.8B parameters)
   - URL: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct
   - Size: ~2.1GB
   - Alternative: Google Gemma-2B (~1.2GB, smaller)

### Step 3: Configure System

Edit `config/settings.yaml`:

```yaml
system:
  name: "Smart Library"
  version: "0.1.0"
  
models:
  stt_model:
    name: "whisper-tiny"
    path: "./data/models/whisper/tiny.en.pt"
    device: "cpu"  # or "cuda" if you have GPU
  
  nlu_model:
    name: "phi-3-mini"
    path: "./data/models/microsoft/Phi-3-mini-4k-instruct"
    quantize: true  # Use 4-bit quantization to save memory

sources:
  open_library:
    enabled: true
    api_key: null  # Not required for basic search
  
  project_gutenberg:
    enabled: true
    base_url: "https://www.gutenberg.org"
  
  archive_org:
    enabled: true
    base_url: "https://archive.org"

pdf:
  font: "Helvetica"
  font_size: 12
  pages_per_response: 2
  
logging:
  level: "INFO"
  file: "./logs/app.log"
```

### Step 4: Run Installation Script

```bash
python install.py
```

This will:
- Verify all dependencies are installed
- Check model files exist
- Create required directories
- Set up environment variables

### Step 5: Start the Application

**Development Mode:**
```bash
# Python implementation
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000

# Node.js implementation
npm run dev
```

**Access the app at:** http://127.0.0.1:8000

---

## Method 2: Docker Installation (Production)

### Step 1: Install Docker Desktop

Download from https://www.docker.com/products/docker-desktop

### Step 2: Build Image

```bash
cd "C:\Users\a11au\OneDrive\Documents\Proj\Smart_Library"
docker-compose build
```

### Step 3: Run Container

```bash
docker-compose up -d
```

View logs:
```bash
docker-compose logs -f
```

### Docker Compose Configuration

See `docker-compose.yml` in the repository.

---

## Model Download Guide (Detailed)

If automatic downloads fail, download manually:

### Whisper Model

**Windows:**
```powershell
# Using git lfs or direct download
Invoke-WebRequest -Uri "https://huggingface.co/openai/whisper-tiny/resolve/main/tiny.en.pt" -OutFile "data\models\whisper\tiny.en.pt"
```

**Linux/macOS:**
```bash
curl -L -o data/models/whisper/tiny.en.pt https://huggingface.co/openai/whisper-tiny/resolve/main/tiny.en.pt
```

### Phi-3 Mini Model

```bash
# Using huggingface-cli
huggingface-cli download microsoft/Phi-3-mini-4k-instruct --local-dir data/models/microsoft/Phi-3-mini-4k-instruct
```

Or using git clone:
```bash
git lfs install
git clone https://huggingface.co/microsoft/Phi-3-mini-4k-instruct data/models/microsoft/Phi-3-mini-4k-instruct
```

---

## Troubleshooting

### Issue: Module Not Found Error

```bash
# Reinstall packages
pip install --force-reinstall --no-deps fastapi uvicorn whisper transformers weasyprint
```

### Issue: CUDA Out of Memory

Edit `config/settings.yaml`:
```yaml
models:
  nlu_model:
    quantize: true  # Enable 4-bit quantization
    device: "cpu"   # Use CPU if GPU runs out of memory
```

### Issue: Model Download Fails (Slow/Time-out)

1. Try downloading via HuggingFace Desktop app instead
2. Use mirror sites if available in your region
3. Reduce download size with smaller models

### Issue: PDF Generation Errors

Ensure WeasyPrint fonts are installed:
```bash
# Windows
scoop install weasyprint-fonts

# Or use system font (Helvetica is usually available)
```

---

## Updating the Application

### Minor Version Updates
```bash
git pull origin main
pip install -r requirements.txt
# Restart application
```

### Model Updates
```bash
python scripts/download_models.py --update
```

---

## Verification

Run these checks to ensure everything is working:

```bash
# Check Python installation
python --version  # Should be 3.10+

# Check dependencies
pip list | findstr whisper  # Should show whisper installed
pip list | findstr transformers

# Test model loading
python scripts/test_models.py

# Check API endpoint
curl http://localhost:8000/docs  # Should show Swagger UI
```

---

## Next Steps

After successful installation:

1. **Read PLANNING.md** to understand the Waterfall Model approach
2. **Review README.md** for architecture overview
3. **Explore the API** at http://localhost:8000/docs
4. **Try recording your first voice query!**

---

## Support

For issues:
1. Check the Troubleshooting section above
2. Review error logs in `./logs/` folder
3. See known issues in `docs/KNOWN_ISSUES.md`

---

**Installation Complete! 🎉**

Your Smart Library app is ready to use. Open your browser and navigate to the application URL, or run your first voice query from the command line interface.
