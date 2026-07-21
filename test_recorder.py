"""Test Script for Voice Recorder Module"""
from src.voice.recorder import VoiceRecorder
import time

print("=" * 60)
print("  Smart Library - Voice Recorder Test")
print("=" * 60 + "\n")

# Initialize recorder
recorder = VoiceRecorder()
print("[OK] Voice Recorder initialized")
print(f"  Sample rate: {recorder.sample_rate} Hz (optimized for Whisper)")
print(f"  Max duration: {recorder.max_duration_seconds}s\n")

# Check microphone availability
if recorder.is_mic_available():
    print("[OK] Microphone is available and detected!")
else:
    print("[WARN] No microphone detected. Please check:")
    print("  - Your system has a working microphone")
    print("  - You're not in a virtual terminal (WSL, Docker)")
    print("  - Windows Privacy settings allow app access to mic\n")

# Start recording session
print("\n--- Starting Recording Test ---\n")
print("Instructions:")
print("  1. Speak into your microphone for up to 60 seconds")
print("  2. Press Ctrl+C when you're done (or wait 5 seconds for auto-stop)")
print("  3. Audio will be saved automatically\n")

try:
    # Start recording
    result = recorder.start_recording()

    if "error" in result:
        print(f"[ERROR] Error starting recording: {result['error']}")
    else:
        print("[OK] Recording started!")
        print(f"  Recording ID: {result['recording_id']}")
        print("\n[INFO] Speaking into microphone now...")

        # Simulate 5 second test recording (replace with user-controlled stop)
        try:
            time.sleep(5)  # Auto-stop after 5 seconds for testing
            print("[TEST] Recording auto-stopped after 5 seconds\n")
        except KeyboardInterrupt:
            print("\n[User interrupted - stopping recording...]")

except KeyboardInterrupt:
    print("\n\n[User interrupted - stopping recording...]")

# Stop and save recording
print("\n--- Saving Audio File ---\n")
try:
    audio_path = recorder.stop_recording()
    if audio_path:
        print(f"[OK] Recording saved to: {audio_path}")

        # Get duration
        duration = recorder.get_duration()
        print(f"[OK] Duration: {duration:.2f} seconds")

except Exception as e:
    print(f"[ERROR] Error saving recording: {e}\n")

print("\n--- Test Complete ---")
print("The voice recorder is ready to use!")
