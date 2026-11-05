# Smart Library — Issues to Fix & Test Plan

> All issues discovered during code review. Each entry includes the problem, suggested fix, and verification tests.

---

## 🔴 Critical Issues

### 1. Tests Call Non-Existent Methods on VoiceRecorder

**File:** `tests/test_voice_module.py` (lines 37, 47, 72)  
**Problem:** Test methods call `self.recorder.stop_recording(session["recording_id"])`, `self.recorder.get_audio()`, and `self.recorder.play_audio()` — none of which exist on the actual `VoiceRecorder` class. The real `stop_recording()` takes no arguments.

**Suggested Fix:**
- Option A: Implement missing methods (`get_audio`, `play_audio`) on `VoiceRecorder`
- Option B: Update tests to match the existing API (remove argument from `stop_recording()`, remove calls to non-existent methods)

**Tests to Verify Fix:**
```bash
cd /home/aumnamaha/Documents/Proj/Smart_Library
python -m pytest tests/test_voice_module.py::TestVoiceRecorder::test_stop_recording_saves_audio -v
python -m pytest tests/test_voice_module.py::TestVoiceRecorder::test_get_audio_retrieves_file -v
python -m pytest tests/test_voice_module.py::TestVoiceRecorder::test_play_audio_calls_player -v
```

---

### 2. Tests Import Non-Existent Names (NameError)

**File:** `tests/test_search_module.py` (lines 64, 79)  
**Problem:** Lines 64 and 79 do:
```python
self.client = OpenLibraryClient()      # NameError — not imported
self.client = ProjectGutenbergClient() # NameError — not imported
```
The test only imports `UnifiedSearchEngine` from the module.

**Suggested Fix:** Add to the import on line 12:
```python
from search.unified_search import UnifiedSearchEngine, OpenLibraryClient, ProjectGutenbergClient
```

**Tests to Verify Fix:**
```bash
cd /home/aumnamaha/Documents/Proj/Smart_Library
python -m pytest tests/test_search_module.py::TestOpenLibraryClient -v
python -m pytest tests/test_search_module.py::TestProjectGutenbergClient -v
```

---

### 3. STT Engine Doesn't Raise on Missing Files

**File:** `tests/test_voice_module.py` (lines 95-96) vs `src/voice/recorder.py`  
**Problem:** Test expects `self.stt_engine.transcribe("nonexistent.wav")` to raise an exception, but the implementation unconditionally returns a placeholder string regardless of whether the file exists.

**Suggested Fix:** In `WhisperSTTEngine.transcribe()`, add a file existence check:
```python
if not os.path.exists(audio_path):
    raise FileNotFoundError(f"Audio file not found: {audio_path}")
```

**Tests to Verify Fix:**
```bash
cd /home/aumnamaha/Documents/Proj/Smart_Library
python -m pytest tests/test_voice_module.py::TestWhisperSTTEngine::test_transcribe_handles_errors -v
# Also manually verify:
python -c "from voice.recorder import WhisperSTTEngine; e = WhisperSTTEngine(); e.transcribe('nonexistent.wav')"
```

---

### 4. PDF Compiler Returns HTML, Not Actual PDF

**File:** `src/pdf_compiler/compiler.py` (line 303)  
**Problem:** The `compile()` method returns `formatted.encode('utf-8')` where `formatted` is an **HTML string**, not valid PDF bytes. Class name and docstrings claim "PDF" but produce HTML. Any consumer expecting a real PDF file will get corrupted data.

**Suggested Fix (Option A — Real PDF):**
Integrate a PDF library like `reportlab`:
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def compile(self, book_info: Dict[str, Any], query: str = "") -> bytes:
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    # ... draw text, headers, footers using reportlab API ...
    c.show_page()
    c.save()
    packet.seek(0)
    return packet.read()
```

**Suggested Fix (Option B — Rename):** If real PDF generation is out of scope, rename the class to `HTMLCompiler` and update all docs/tests accordingly.

**Tests to Verify Fix:**
```bash
cd /home/aumnamaha/Documents/Proj/Smart_Library
python -m pytest tests/test_pdf_module.py::TestPDFCompiler::test_compile_returns_pdf_bytes -v
# Additional manual test:
python -c "
from pdf_compiler.compiler import PDFCompiler
compiler = PDFCompiler()
book_info = {'title': 'Test', 'author': 'Author', 'isbn': '123', 'source': 'test'}
pdf_bytes = compiler.compile(book_info)
print('Starts with PDF header:', pdf_bytes[:5] == b'%PDF-')
"
```

---

### 5. Hardcoded Confidence Scoring in Search Engine

**File:** `src/search/unified_search.py` (lines 224-231)  
**Problem:** The `_calculate_confidence()` method is hardcoded to specific book/author strings:
```python
if "wings of fire" in query_lower and title.lower().find("wings") != -1:
    return 0.95
elif "apj kalam" in query_lower:
    return 0.85
```
The comment on line 220 says "use Levenshtein distance" but no fuzzy matching is implemented.

**Suggested Fix:** Replace with a general-purpose fuzzy match using `fuzzywuzzy` or `rapidfuzz`:
```python
from rapidfuzz import fuzz

def _calculate_confidence(self, query: str, title: str, author: str) -> float:
    query_lower = query.lower()
    title_lower = title.lower()
    # Exact match
    if query_lower == title_lower:
        return 1.0
    # Partial match using Levenshtein distance
    title_ratio = fuzz.ratio(query_lower, title_lower) / 100.0
    author_ratio = fuzz.ratio(query_lower, author.lower()) / 100.0 if author else 0.0
    return max(title_ratio, author_ratio * 0.7)
```

**Tests to Verify Fix:**
```bash
cd /home/aumnamaha/Documents/Proj/Smart_Library
python -m pytest tests/test_search_module.py::TestUnifiedSearchEngine::test_search_calculates_confidence -v
python -m pytest tests/test_search_module.py::TestUnifiedSearchEngine::test_search_sorts_by_confidence -v
# Manual test with various queries:
python -c "
from search.unified_search import UnifiedSearchEngine
engine = UnifiedSearchEngine()
r1 = engine.search('Wings of Fire')
r2 = engine.search('The Alchemist')
print('Results for Wings of Fire:', [(b['title'], b['confidence']) for b in r1])
print('Results for The Alchemist:', [(b['title'], b['confidence']) for b in r2])
"
```

---

## 🟡 Moderate Issues

### 6. Missing numpy Import — NameError in get_remaining_time()

**File:** `src/voice/recorder.py` (line ~312-313)  
**Problem:** `get_remaining_time()` uses `np.asarray(self._recording_obj)` but `numpy` is never imported at the module level. Will crash with `NameError`.

**Suggested Fix:** Add to imports:
```python
import numpy as np
```

**Tests to Verify Fix:**
```bash
cd /home/aumnamaha/Documents/Proj/Smart_Library
python -c "from voice.recorder import VoiceRecorder; r = VoiceRecorder(); r.get_remaining_time()"
# Should not raise NameError
```

---

### 7. Model Cache Stores Strings Instead of Models

**File:** `src/models/model_runner.py` (line ~58)  
**Problem:** The model cache stores a formatted string instead of an actual model object:
```python
self.model_cache[model_name] = f"Model[{model_name}] instance loaded to {self.MODELS_DIR}"
```
The docstring says "Loaded model instance" but returns a string.

**Suggested Fix:** Either store the real model object, or update the docstring and return type annotation to reflect that this is a placeholder/stub implementation.

**Tests to Verify Fix:**
```bash
cd /home/aumnamaha/Documents/Proj/Smart_Library
python -c "
from models.model_runner import SpeechToTextRunner
runner = SpeechToTextRunner({'stt_model_name': 'whisper-tiny'})
model = runner.load_model('whisper-tiny')
print('Type:', type(model))
print('Is string:', isinstance(model, str))  # Should be False after fix
"
```

---

### 8. Language Manager — KeyError on Missing YAML Keys

**File:** `src/voice/language_manager.py` (lines ~179-180)  
**Problem:** When writing config:
```python
config['system']['version'] = "0.2.0"
```
If the YAML file lacks a `system` key, this raises `KeyError`. The same pattern appears in `select_language()`.

**Suggested Fix:** Use `.setdefault()` to safely create nested keys:
```python
config.setdefault('system', {})['version'] = "0.2.0"
```

**Tests to Verify Fix:**
```bash
cd /home/aumnamaha/Documents/Proj/Smart_Library
# Create a minimal YAML without 'system' key
echo '{"language": {"default": "en"}}' | python -c "
import yaml, sys
config = {'language': {'default': 'en'}}
with open('/tmp/test_config.yaml', 'w') as f:
    yaml.dump(config, f)

from voice.language_manager import LanguageManager
lm = LanguageManager()
# Should not raise KeyError
try:
    lm.save_user_preference()  # or whatever method triggers the write
    print('OK — no KeyError')
except KeyError as e:
    print(f'FAIL — KeyError: {e}')
"
```

---

### 9. `save_user_preference` Has Dead Code

**File:** `src/voice/language_manager.py` (line ~256)  
**Problem:** The method calls `self._load_config()` but never uses any config values — it just writes a marker file. The reload is unnecessary overhead.

**Suggested Fix:** Remove the `_load_config()` call:
```python
def save_user_preference(self):
    marker_path = "./data/language_selection_completed"
    if not os.path.exists(marker_path):
        with open(marker_path, 'w') as f:
            f.write(f"Saved at {datetime.now().isoformat()}\n")
```

**Tests to Verify Fix:**
```bash
cd /home/aumnamaha/Documents/Proj/Smart_Library
python -c "
from voice.language_manager import LanguageManager
import os, tempfile
# Point config to temp dir
lm = LanguageManager('/tmp/test_lang_settings.yaml')
lm.save_user_preference()
assert os.path.exists('./data/language_selection_completed'), 'Marker file not created'
print('OK — marker file created successfully')
"
```

---

### 10. API PDF Download Endpoint Returns Raw Bytes Incorrectly

**File:** `src/api/server.py` (line ~297)  
**Problem:** The `/pdf/download/{job_id}` endpoint returns raw bytes:
```python
return pdf_bytes
```
FastAPI will wrap this as JSON instead of sending it as a file download. Should use `FileResponse`.

**Suggested Fix:**
```python
from fastapi.responses import FileResponse

@app.get("/pdf/download/{job_id}")
async def download_pdf(job_id: str):
    pdf_path = os.path.join(pdf_compiler.config["output_dir"], f"{job_id}.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"{job_id}.pdf")
```

**Tests to Verify Fix:**
```bash
cd /home/aumnamaha/Documents/Proj/Smart_Library
# Start server and test:
uvicorn src.api.server:app --port 8001 &
sleep 2
curl -s -o /dev/null -w "%{http_code} %{content_type}" http://localhost:8001/pdf/download/test-job-123
# Should return 200 with content-type application/pdf, not text/html or application/json
kill %1 2>/dev/null
```

---

## 🟢 Minor Issues / Code Quality

### 11. Deprecated Type Hints — `dict[str, any]` instead of `Dict[str, Any]`

**File:** `src/voice/recorder.py` (line ~68)  
**Problem:** Uses lowercase `dict[str, any]` which is deprecated in Python < 3.9 and inconsistent with the rest of the codebase that uses `typing.Dict`.

**Suggested Fix:** Replace all instances:
```python
# Before:
def method(self) -> dict[str, any]: ...

# After:
from typing import Dict, Any
def method(self) -> Dict[str, Any]: ...
```

**Tests to Verify Fix:**
```bash
cd /home/aumnamaha/Documents/Proj/Smart_Library
python -W error::DeprecationWarning -c "import voice.recorder"
# Should not emit any deprecation warnings
```

---

### 12. Unused `sys` and `os` Imports in API Server

**File:** `src/api/server.py` (lines 18-19)  
**Problem:** `import sys` and `import os` are present but unused (the path insertion on line 22 was removed).

**Suggested Fix:** Remove both imports. If `os.popen('date')` is needed for the health endpoint, import only what's used:
```python
from datetime import datetime
# Replace os.popen('date').read().strip() with datetime.now().isoformat()
```

**Tests to Verify Fix:**
```bash
cd /home/aumnamaha/Documents/Proj/Smart_Library
python -c "import ast; tree = ast.parse(open('src/api/server.py').read()); imports = [n.names[0].name for n in ast.walk(tree) if isinstance(n, ast.Import)]; print('Unused:', set(imports))"
# Should not list 'sys' or 'os' as unused
```

---

### 13. Timestamp Inconsistency — `os.popen('date')` vs `datetime.now()`

**File:** `src/api/server.py` (line ~303)  
**Problem:** Health endpoint uses `os.popen('date').read().strip()` instead of the standard `datetime.now().isoformat()` used elsewhere in the codebase.

**Suggested Fix:**
```python
from datetime import datetime

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

**Tests to Verify Fix:**
```bash
cd /home/aumnamaha/Documents/Proj/Smart_Library
uvicorn src.api.server:app --port 8002 &
sleep 2
curl -s http://localhost:8002/health | python -m json.tool
# Should return ISO-format timestamp, not raw date string
kill %1 2>/dev/null
```

---

### 14. Unused `page_number` and `total_pages` in PDF Compiler Metadata

**File:** `src/pdf_compiler/compiler.py` (lines ~297-298)  
**Problem:** `"page_number": 1, "total_pages": "dynamic"` are set in metadata but never used anywhere in the pipeline.

**Suggested Fix:** Either remove these fields or implement actual pagination tracking during PDF generation.

**Tests to Verify Fix:**
```bash
cd /home/aumnamaha/Documents/Proj/Smart_Library
grep -rn "page_number\|total_pages" src/pdf_compiler/compiler.py tests/test_pdf_module.py
# After fix: either both are used end-to-end, or neither exists
```

---

### 15. Windows Path in Documentation

**File:** `docs/WATERFALL_SUMMARY.md` (line ~154)  
**Problem:** Contains hardcoded Windows path:
```bash
cd "C:\Users\a11au\OneDrive\Documents\Proj\Smart_Library"
```
This is not cross-platform and exposes a personal OneDrive path.

**Suggested Fix:** Replace with a generic placeholder:
```bash
cd <project_root>
# or use $PWD for cross-platform compatibility
```

**Tests to Verify Fix:**
```bash
grep -n "C:\\\\Users" docs/WATERFALL_SUMMARY.md
# Should return no results after fix
```

---

### 16. WhisperSTTEngine Accepts Unused `language_manager` Parameter

**File:** `src/voice/recorder.py` (line ~402)  
**Problem:** `WhisperSTTEngine.__init__` accepts `language_manager=None` but never uses it in `transcribe()`. The parameter is accepted and checked as a truthy value but has no effect.

**Suggested Fix:** Either:
- Remove the unused parameter, or
- Actually use it to set the transcription language (e.g., pass to Whisper's `language` argument)

**Tests to Verify Fix:**
```bash
cd /home/aumnamaha/Documents/Proj/Smart_Library
python -c "
from voice.recorder import WhisperSTTEngine, LanguageManager
lm = LanguageManager()
engine = WhisperSTTEngine(language_manager=lm)
# After fix: either the parameter is removed (raises TypeError), or language is actually applied
"
```

---

## 📋 Master Test Suite — Run All Fixes at Once

After applying all fixes above, run this comprehensive test command:

```bash
cd /home/aumnamaha/Documents/Proj/Smart_Library

# 1. Run all unit tests
python -m pytest tests/ -v --tb=short

# 2. Check for unused imports across the codebase
pip install flake8 > /dev/null 2>&1
flake8 src/ --select=F401 --ignore=E501,W503

# 3. Type check (if mypy is available)
pip install mypy > /dev/null 2>&1
mypy src/ --ignore-missing-imports

# 4. Verify no hardcoded paths in docs
grep -rn "C:\\\\Users" docs/ || echo "No Windows paths found — OK"

# 5. Verify PDF output is valid (if real PDF fix applied)
python -c "
from pdf_compiler.compiler import PDFCompiler
compiler = PDFCompiler()
book_info = {'title': 'Test', 'author': 'Author', 'isbn': '123', 'source': 'test'}
pdf_bytes = compiler.compile(book_info)
assert pdf_bytes[:5] == b'%PDF-', f'Expected PDF header, got: {pdf_bytes[:20]}'
print('PASS — Valid PDF output')
"

# 6. Verify search confidence is generalized (not hardcoded)
python -c "
from search.unified_search import UnifiedSearchEngine
engine = UnifiedSearchEngine()
r1 = engine.search('Wings of Fire')
r2 = engine.search('Completely Unknown Book XYZ 99999')
# Both should return results with reasonable confidence scores
for r in [r1, r2]:
    for book in r:
        assert 'confidence' in book, f'Missing confidence in {book}'
        assert 0 <= book['confidence'] <= 1.0, f'Invalid confidence: {book[\"confidence\"]}'
print('PASS — Confidence scoring works for arbitrary queries')
"

# 7. Verify API server starts and health endpoint returns ISO timestamp
uvicorn src.api.server:app --port 8099 &
sleep 2
TIMESTAMP=$(curl -s http://localhost:8099/health | python -c "import sys,json; print(json.load(sys.stdin)['timestamp'])")
python -c "from datetime import datetime; datetime.fromisoformat('$TIMESTAMP'); print('PASS — ISO timestamp')" &
sleep 1
kill %1 2>/dev/null

# 8. Verify language manager handles missing keys gracefully
python -c "
import yaml, os
os.makedirs('/tmp/test_lang', exist_ok=True)
with open('/tmp/test_lang/settings.yaml', 'w') as f:
    yaml.dump({'language': {'default': 'en'}}, f)

from voice.language_manager import LanguageManager
lm = LanguageManager('/tmp/test_lang/settings.yaml')
try:
    lm.save_user_preference()  # or trigger the write path
    print('PASS — No KeyError on missing keys')
except KeyError as e:
    print(f'FAIL — KeyError: {e}')
"

# Cleanup
rm -rf /tmp/test_lang /tmp/test_config.yaml ./data/language_selection_completed ./data/audio/recordings_test ./data/generated_pdf_test 2>/dev/null
```

---

## 📊 Summary Table

| # | Severity | File | Issue | Quick Fix? |
|---|----------|------|-------|------------|
| 1 | 🔴 Critical | `tests/test_voice_module.py` | Tests call non-existent methods | Yes — update tests or implement methods |
| 2 | 🔴 Critical | `tests/test_search_module.py` | NameError — missing imports | Yes — add imports |
| 3 | 🔴 Critical | `src/voice/recorder.py` + test | STT doesn't raise on missing file | Yes — add file check |
| 4 | 🔴 Critical | `src/pdf_compiler/compiler.py` | Returns HTML, not PDF | Medium — integrate reportlab or rename |
| 5 | 🔴 Critical | `src/search/unified_search.py` | Hardcoded confidence scoring | Medium — add rapidfuzz dependency |
| 6 | 🟡 Moderate | `src/voice/recorder.py` | Missing numpy import | Yes — add `import numpy as np` |
| 7 | 🟡 Moderate | `src/models/model_runner.py` | Cache stores strings, not models | Yes — fix or update docs |
| 8 | 🟡 Moderate | `src/voice/language_manager.py` | KeyError on missing YAML keys | Yes — use `.setdefault()` |
| 9 | 🟡 Moderate | `src/voice/language_manager.py` | Dead code in `save_user_preference` | Yes — remove `_load_config()` call |
| 10 | 🟡 Moderate | `src/api/server.py` | PDF download returns raw bytes | Yes — use `FileResponse` |
| 11 | 🟢 Minor | `src/voice/recorder.py` | Deprecated type hints | Yes — use `Dict[str, Any]` |
| 12 | 🟢 Minor | `src/api/server.py` | Unused imports (`sys`, `os`) | Yes — remove them |
| 13 | 🟢 Minor | `src/api/server.py` | Non-ISO timestamp in health check | Yes — use `datetime.now()` |
| 14 | 🟢 Minor | `src/pdf_compiler/compiler.py` | Unused metadata fields | Optional — clean up or implement |
| 15 | 🟢 Minor | `docs/WATERFALL_SUMMARY.md` | Windows path in docs | Yes — replace with placeholder |
| 16 | 🟢 Minor | `src/voice/recorder.py` | Unused `language_manager` param | Optional — remove or implement |

**Total: 16 issues (5 critical, 5 moderate, 6 minor)**
