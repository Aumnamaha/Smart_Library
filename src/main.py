"""
Smart Library Application - Main Entry Point
============================================

Waterfall Model Implementation Summary:
- Phase 1 (Requirements): COMPLETED ✅
- Phase 2 (Design): COMPLETED ✅
- Phase 3 (Implementation): IN PROGRESS 🔄
- Phase 4 (Testing): PENDING ⏳
- Phase 5 (Deployment): PENDING ⏳
- Phase 6 (Maintenance): PLANNED ⏳

Usage:
    python -m src.main              # Run application directly
    uvicorn src.main:app --reload   # Run as FastAPI server
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice.recorder import VoiceRecorder, WhisperSTTEngine
from models.model_runner import SpeechToTextRunner, NLUModelRunner
from search.unified_search import UnifiedSearchEngine
from pdf_compiler.compiler import PDFCompiler


class SmartLibraryApp:
    """
    Main application class coordinating all components.

    Architecture Flow:
        Voice Input → STT Model → NLU Model → Search Engine → PDF Compiler → Download
    """

    def __init__(self, config_path: str = "./config/settings.yaml"):
        self.config_path = config_path

        # Initialize components in order (dependency injection)
        self.voice_recorder = VoiceRecorder()
        self.stt_engine = WhisperSTTEngine()

        # Model runners with shared configuration
        self.config = {
            "stt_model_name": "whisper-tiny",
            "nlu_model_name": "phi-3-mini"
        }
        self.stt_runner = SpeechToTextRunner(self.config)
        self.nlu_runner = NLUModelRunner(self.config)

        # Search and PDF components
        search_config = {
            "open_library_api_key": None,
            "disabled_sources": []
        }
        self.search_engine = UnifiedSearchEngine(search_config)
        self.pdf_compiler = PDFCompiler()

    def start_session(self):
        """Start a new voice recording session."""
        print("\n" + "="*60)
        print("  Smart Library - Voice-Powered Book Finder")
        print("="*60)

        result = self.voice_recorder.start_recording()
        return result

    def stop_session(self, session_id: str) -> str:
        """Stop recording and get audio file path."""
        return self.voice_recorder.stop_recording(session_id)

    def transcribe(self, audio_path: str) -> str:
        """Transcribe audio to text using STT model."""
        print(f"\n[STT] Processing audio file...")
        transcript = self.stt_engine.transcribe(audio_path)
        print(f"[STT] Transcript: {transcript[:100]}...")
        return transcript

    def parse_query(self, transcript: str) -> dict:
        """Parse transcript using NLU model."""
        print("\n[NLU] Parsing voice query...")
        parsed = self.nlu_runner.parse_query(transcript)

        print(f"[NLU] Extracted:")
        print(f"  Title: {parsed.get('title', 'Not specified')}")
        print(f"  Author: {parsed.get('author', 'Not specified')}")
        print(f"  Intent: {parsed.get('intent', '')}")

        return parsed

    def search_books(self, parsed_query: dict) -> list:
        """Search for matching books."""
        # Build query string from parsed info
        query_str = f"{parsed_query.get('title', 'book')} {parsed_query.get('author', '')}"

        print(f"\n[Search] Searching for: {query_str}")
        results = self.search_engine.search(query_str)

        print(f"[Search] Found {len(results)} matches:")
        for i, book in enumerate(results[:3], 1):
            confidence = book.get('confidence', 0)
            print(f"  {i}. {book['title']} by {book['author']}")
            print(f"      Source: {book['source']}, Confidence: {confidence:.2f}")

        return results

    def compile_pdf(self, book_info: dict, query: str) -> bytes:
        """Generate PDF excerpt."""
        print(f"\n[PDF] Generating 2-page excerpt...")
        pdf_bytes = self.pdf_compiler.compile(book_info, query)
        print(f"[PDF] Generated {len(pdf_bytes)} bytes")

        return pdf_bytes

    def run_query_flow(self):
        """Execute complete voice-to-PDF flow."""
        try:
            # 1. Start recording
            session = self.start_session()
            print(f"\n[Voice] Recording started: {session['recording_id']}")
            print("   Speak your query (max 60 seconds):")
            print("   Example: 'I want to read Wings of Fire by apj kalam'")

            # Simulate user speaking...
            import time
            time.sleep(5)  # In real app, user controls duration

            # 2. Stop recording
            audio_path = self.stop_session(session['recording_id'])
            print(f"\n[Voice] Recording saved: {audio_path}")

            # 3. Transcribe
            transcript = self.transcribe(audio_path)

            # 4. Parse query
            parsed = self.parse_query(transcript)

            # 5. Search books
            results = self.search_books(parsed)

            if not results:
                print("\n[Search] No books found matching your query.")
                return None

            # Select best match
            best_match = results[0]

            # 6. Generate PDF
            pdf_bytes = self.compile_pdf(best_match, transcript)

            # 7. Return result (in real app, save and provide download link)
            print("\n" + "="*60)
            print("  RESULTS!")
            print("="*60)
            print(f"\nBook: {best_match['title']}")
            print(f"Author: {best_match['author']}")
            print(f"Source: {best_match['source']}")
            print("\nPDF ready for download!")

            return {
                "book": best_match,
                "query": transcript,
                "pdf_bytes": pdf_bytes
            }

        except Exception as e:
            print(f"\n[ERROR] Error during query processing: {str(e)}")
            raise


# Main application entry point
app = SmartLibraryApp()

if __name__ == "__main__":
    # Interactive mode for testing
    import readline  # Enable command history

    print("\n" + "="*60)
    print("  Smart Library - Interactive Mode")
    print("="*60)
    print("\nType 'query' to run a voice query flow.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            command = input("> ").strip()

            if command.lower() == "exit":
                break
            elif command.lower() == "query":
                result = app.run_query_flow()
                if result:
                    print(f"\nDownload PDF (simulated): {len(result['pdf_bytes'])} bytes")
            else:
                print(f"Unknown command: {command}")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
