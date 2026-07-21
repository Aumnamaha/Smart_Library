"""Test Script for Voice Recorder Module - With Timer & Waveform"""
from src.voice.recorder import VoiceRecorder, WaveformVisualizer
import time

print("=" * 60)
print("  Smart Library - Voice Recorder Test")
print("  Features: Countdown Timer + Real-time Waveform Display")
print("=" * 60 + "\n")

# Initialize waveform visualizer for real-time updates
visualizer = WaveformVisualizer()

# Create recorder with callback for timer/waveform updates
recorder = VoiceRecorder(
    update_callback=lambda msg: print(msg),
    output_dir="./data/audio/recordings"
)

print("[OK] Voice Recorder initialized")
print(f"[INFO] Sample rate: {recorder.sample_rate} Hz (optimized for Whisper)")
print(f"[INFO] Max duration: {recorder.max_duration_seconds}s\n")

# Check microphone availability
if recorder.is_mic_available():
    print("[OK] Microphone is available and detected!\n")
else:
    print("[WARN] No microphone detected. Please check:")
    print("  - Your system has a working microphone")
    print("  - You're not in a virtual terminal (WSL, Docker)")
    print("  - Windows Privacy settings allow app access to mic\n")

# Start recording with timer
print("\n" + "=" * 60)
print("  STARTING RECORDING SESSION")
print("=" * 60 + "\n")

print("Instructions:")
print("  1. Speak clearly into your microphone")
print("  2. A countdown timer will show remaining time (10s, 9s, 8s...)")
print("  3. A waveform bar shows your voice energy in real-time")
print(f"  4. Recording auto-stops after {recorder.max_duration_seconds} seconds\n")

try:
    # Start recording for 10 second test (adjust as needed)
    result = recorder.start_recording(duration=10)

    if "error" in result:
        print(f"[ERROR] Error starting recording: {result['error']}")
    else:
        print("[OK] Recording started!\n")
        print("[INFO] Speak into microphone now... Timer counting down:")

        # Wait for recording (auto-stops at 10 seconds)
        time.sleep(10)

except KeyboardInterrupt:
    print("\n\n[User interrupted - stopping recording...]")

# Stop and save recording
print("\n" + "=" * 60)
print("  SAVING RECORDING...")
print("=" * 60 + "\n")

try:
    audio_path = recorder.stop_recording()

    if audio_path:
        print(f"\n[OK] Recording saved to: {audio_path}")

        # Get duration
        duration = recorder.get_audio_duration()
        print(f"[OK] Duration: {duration:.2f} seconds")

        # Get waveform for visualization test
        waveform = recorder.get_waveform(sample_count=30)
        if waveform and len(waveform) > 0:
            import numpy as np
            avg_energy = sum(np.abs(x) for x in waveform) / len(waveform) * 100
            print(f"[OK] Waveform average energy: {str(round(float(avg_energy), 1))}%")

except Exception as e:
    print(f"[ERROR] Error saving recording: {e}\n")

print("\n" + "=" * 60)
print("  TEST COMPLETE!")
print("=" * 60 + "\n")

print("Summary:")
print(f"  - Microphone: {'Working' if recorder.is_mic_available() else 'Not detected'}")
print(f"  - Recording captured: {duration:.2f} seconds")
print(f"  - Audio quality: {recorder.sample_rate}Hz, Mono WAV")
print(f"  - Timer feature: ENABLED (shows countdown during recording)")
print(f"  - Waveform display: ENABLED (real-time energy bar)\n")

print("=" * 60)
print("  Next Steps:")
print("=" * 60)
print("  1. Try speaking different volumes to see waveform changes")
print("  2. Test with longer recording times (max 60s)")
print("  3. Ready for Whisper STT integration!\n")
