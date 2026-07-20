"""
Test Suite: Voice Module
=========================

Waterfall Model Phase: Testing (Phase 4)
Tests for FR-01 (Voice Input System) and FR-02 (STT Transcription)
"""

import sys
import os
import unittest
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from voice.recorder import VoiceRecorder, WhisperSTTEngine


class TestVoiceRecorder(unittest.TestCase):
    """Test cases for VoiceRecorder class."""

    def setUp(self):
        self.output_dir = "./data/audio/recordings_test"
        os.makedirs(self.output_dir, exist_ok=True)
        self.recorder = VoiceRecorder(self.output_dir)

    def test_start_recording_creates_session(self):
        """Test: Start recording creates valid session."""
        result = self.recorder.start_recording()

        self.assertIn("recording_id", result)
        self.assertIn("session_started", result)
        self.assertTrue(result["session_started"])

    def test_stop_recording_saves_audio(self):
        """Test: Stop recording saves audio to file."""
        session = self.recorder.start_recording()
        audio_path = self.recorder.stop_recording(session["recording_id"])

        self.assertIsNotNone(audio_path)
        self.assertIn(".wav", audio_path.lower())

    def test_get_audio_retrieves_file(self):
        """Test: Get audio retrieves saved file."""
        session = self.recorder.start_recording()
        audio_path = self.recorder.stop_recording(session["recording_id"])

        result = self.recorder.get_audio(session["recording_id"])
        self.assertIn(".wav", result.lower())

    def test_play_audio_calls_player(self):
        """Test: Play audio triggers playback."""
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_path = f.name

        try:
            # Mock the player to verify it's called
            original_print = print
            printed_messages = []

            def mock_print(*args):
                printed_messages.append(args[0])

            # Create temporary WAV file
            import wave
            with wave.open(temp_path, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(16000)

            self.recorder.play_audio(temp_path)

            self.assertIn("[Voice Player]", printed_messages[0])
        finally:
            os.unlink(temp_path)


class TestWhisperSTTEngine(unittest.TestCase):
    """Test cases for Whisper STT engine."""

    def setUp(self):
        self.stt_engine = WhisperSTTEngine()

    def test_transcribe_returns_string(self):
        """Test: Transcribe returns transcribed text."""
        result = self.stt_engine.transcribe("test_audio.wav")

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_transcribe_handles_errors(self):
        """Test: STT handles invalid audio gracefully."""
        # This should raise appropriate error or return empty string
        with self.assertRaises(Exception):
            self.stt_engine.transcribe("nonexistent.wav")


if __name__ == "__main__":
    unittest.main()
