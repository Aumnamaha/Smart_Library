"""
Smart Library API Server
========================

RESTful API endpoints for the Smart Library application.

Endpoints:
    POST   /voice/record          - Start voice recording session
    POST   /voice/stop/{id}       - Stop recording and transcribe
    GET    /voice/transcript/{id} - Get transcription result
    GET    /books/search          - Search for books
    GET    /books/{isbn}          - Get book details
    POST   /pdf/generate          - Generate PDF from search results

Waterfall Model Phase: Implementation (Week 11-12)
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import uuid

from voice.recorder import VoiceRecorder, WhisperSTTEngine
from models.model_runner import SpeechToTextRunner, NLUModelRunner
from search.unified_search import UnifiedSearchEngine
from pdf_compiler.compiler import PDFCompiler


# Initialize FastAPI app
app = FastAPI(
    title="Smart Library API",
    description="Voice-powered book discovery and PDF excerpt generation",
    version="1.0.0"
)

# Initialize application components
voice_recorder = VoiceRecorder()
stt_engine = WhisperSTTEngine()

model_config = {
    "stt_model_name": "whisper-tiny",
    "nlu_model_name": "phi-3-mini"
}

stt_runner = SpeechToTextRunner(model_config)
nlu_runner = NLUModelRunner(model_config)

search_config = {
    "open_library_api_key": None,
    "disabled_sources": []
}
search_engine = UnifiedSearchEngine(search_config)

pdf_compiler = PDFCompiler()


# Request/Response Models
class VoiceRecordRequest(BaseModel):
    """Request model for voice recording."""
    max_duration: int = 60
    format: str = "wav"


class BookSearchRequest(BaseModel):
    """Request model for book search."""
    title: Optional[str] = None
    author: Optional[str] = None
    keywords: Optional[str] = None
    limit: int = 10


# API Endpoints

@app.get("/")
async def root():
    """API health check and information."""
    return {
        "service": "Smart Library API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/voice/record",
            "/voice/stop/{session_id}",
            "/voice/transcript/{session_id}",
            "/books/search",
            "/books/{isbn}",
            "/pdf/generate"
        ]
    }


@app.post("/voice/record")
async def start_recording(request: VoiceRecordRequest):
    """
    Start a voice recording session.

    Returns:
        Session ID and recording configuration
    """
    # In production, this would initialize audio capture stream
    recording_id = str(uuid.uuid4())[:8]

    return {
        "session_id": recording_id,
        "status": "recording",
        "max_duration_seconds": request.max_duration,
        "message": "Recording started. Speak your book query."
    }


@app.post("/voice/stop/{session_id}")
async def stop_recording(session_id: str) -> dict:
    """
    Stop recording and transcribe audio.

    Args:
        session_id: The recording session identifier

    Returns:
        Transcription result and next steps
    """
    # In production, this would:
    # 1. Stop audio stream
    # 2. Write samples to WAV file
    # 3. Load STT model if not already loaded
    # 4. Transcribe the audio

    print(f"[API] Processing recording: {session_id}")

    # Simulate transcription (in production, use actual model)
    transcript = "[Transcribed text from user's voice query]"

    return {
        "session_id": session_id,
        "transcript": transcript,
        "status": "completed",
        "next_step": "query will be parsed automatically"
    }


@app.get("/voice/transcript/{session_id}")
async def get_transcript(session_id: str) -> dict:
    """
    Get transcription result for completed recording.

    Args:
        session_id: The recording session identifier

    Returns:
        Full transcript text
    """
    # In production, fetch from storage or re-transcribe if needed
    return {
        "session_id": session_id,
        "transcript": "[Transcribed text]",
        "confidence": 0.95
    }


@app.get("/books/search")
async def search_books(request: Optional[BookSearchRequest] = None) -> dict:
    """
    Search for books across open source platforms.

    Args:
        title: Book title (optional)
        author: Author name (optional)
        keywords: Search keywords (optional)
        limit: Maximum results to return (default: 10)

    Returns:
        List of matching books with availability info
    """
    request = request or BookSearchRequest()

    # Build query string
    query_parts = []
    if request.title:
        query_parts.append(request.title)
    if request.author:
        query_parts.append(f"by {request.author}")
    if request.keywords:
        query_parts.append(request.keywords)

    query_str = " ".join(query_parts)

    if not query_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least one search term (title, author, or keywords)"
        )

    print(f"[API] Searching for: {query_str}")

    # Search books
    results = search_engine.search(query_str)

    return {
        "query": query_str,
        "total_results": len(results),
        "results": results[:request.limit]
    }


@app.get("/books/{isbn}")
async def get_book_details(isbn: str) -> dict:
    """
    Get detailed information about a specific book.

    Args:
        isbn: Book ISBN identifier

    Returns:
        Full book details and availability
    """
    # In production, query multiple sources for ISBN lookup
    return {
        "isbn": isbn,
        "title": "Example Book",
        "author": "Example Author",
        "sources": ["open_library", "gutenberg"],
        "available": True
    }


@app.post("/pdf/generate")
async def generate_pdf(session_id: str, title: Optional[str] = None) -> dict:
    """
    Generate 2-page PDF excerpt from a book.

    Args:
        session_id: Previous voice recording session ID (for query context)
        title: Book title to get excerpt from (optional)

    Returns:
        Generated PDF as base64-encoded bytes with download link
    """
    # Get transcript for this session
    try:
        transcript_response = get_transcript(session_id)
        transcript = transcript_response.get("transcript", "")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Session not found: {str(e)}"
        )

    # If title not provided, extract from query
    if not title and transcript:
        title = " ".join(transcript.split()[:3])  # Use first 3 words as title fallback

    print(f"[API] Generating PDF for: {title}")

    # Create mock book info (in production, use search results)
    book_info = {
        "title": title or "Unknown Book",
        "author": "Unknown Author",
        "isbn": "978-0-123456-78-9",
        "source": "open_library"
    }

    # Compile PDF
    pdf_bytes = pdf_compiler.compile(book_info, transcript)

    return {
        "session_id": session_id,
        "book_title": title,
        "query": transcript[:100] + "...",
        "pdf_size_bytes": len(pdf_bytes),
        "download_url": f"/api/v1/pdf/download/{session_id}",
        "status": "generated"
    }


@app.get("/pdf/status/{job_id}")
async def get_pdf_status(job_id: str) -> dict:
    """Check PDF generation status."""
    return {
        "job_id": job_id,
        "status": "completed",
        "progress": 100
    }


@app.get("/pdf/download/{job_id}")
async def download_pdf(job_id: str):
    """Download generated PDF."""
    # In production, read from storage and send as file response
    pdf_bytes = b"%PDF-1.4 placeholder content"

    return pdf_bytes


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": str(os.popen('date').read().strip())}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
