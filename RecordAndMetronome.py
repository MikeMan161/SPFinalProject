from pydub import AudioSegment
from pydub.playback import play
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import threading
import time

# Function to play the metronome
def metronome(bpm, duration, stop_event):
    """Plays a metronome click at the given BPM for the specified duration."""
    tick = AudioSegment.from_file('tick.wav')  # Load the tick sound
    interval = 60 / bpm  # Time interval between beats
    print(f"Metronome started at {bpm} BPM for {duration} seconds.")
    start_time = time.perf_counter()
    next_tick_time = start_time

    try:
        while not stop_event.is_set() and time.perf_counter() - start_time < duration:
            current_time = time.perf_counter()

            if current_time >= next_tick_time:
                play(tick)  # Play the tick sound
                next_tick_time += interval  # Schedule the next tick

            time.sleep(0.001)  # Small sleep for responsiveness
    except Exception as e:
        print(f"\nMetronome stopped due to: {e}")

    print("Metronome completed.")

# Function to record audio
def record_audio(duration, output_file, stop_event):
    """Records audio for the specified duration."""
    print(f"Recording audio for {duration} seconds... Press Ctrl+C to stop.")
    sample_rate = 44100  # Sample rate
    recorded_frames = []
    end_time = time.time() + duration

    try:
        while not stop_event.is_set() and time.time() < end_time:
            # Record short chunks of audio (e.g., 1 second)
            chunk = sd.rec(int(sample_rate * 1), samplerate=sample_rate, channels=2, dtype='float64')
            sd.wait()
            recorded_frames.append(chunk)
    except Exception as e:
        print(f"\nRecording stopped due to: {e}")
    
    # Combine all recorded frames
    recording = np.concatenate(recorded_frames, axis=0)
    write(output_file, sample_rate, (recording * 32767).astype(np.int16))
    print(f"Audio saved as {output_file}")

# Function to start the metronome and/or recording based on user input
def start_program():
    """Prompts user for metronome and recording preferences and runs the program."""
    stop_event = threading.Event()
    
    # Prompt for metronome
    metronome_choice = input("Would you like to enable the metronome? (yes/no): ").strip().lower()
    metronome_thread = None
    if metronome_choice == "yes":
        bpm = int(input("Enter the BPM for the metronome: "))
        duration = int(input("Enter the duration for the metronome (in seconds): "))
        metronome_thread = threading.Thread(target=metronome, args=(bpm, duration, stop_event))

    # Prompt for recording
    record_choice = input("Would you like to record audio? (yes/no): ").strip().lower()
    recording_thread = None
    if record_choice == "yes":
        recording_duration = int(input("Enter the duration for recording (in seconds): "))
        output_file = input("Enter the output file name (e.g., output.wav): ").strip()
        recording_thread = threading.Thread(target=record_audio, args=(recording_duration, output_file, stop_event))

    # Start selected threads
    if metronome_thread:
        metronome_thread.start()
    if recording_thread:
        recording_thread.start()

    try:
        # Wait for threads to finish
        if metronome_thread:
            metronome_thread.join()
        if recording_thread:
            recording_thread.join()
    except KeyboardInterrupt:
        stop_event.set()  # Signal threads to stop
        print("\nStopping threads...")
        if metronome_thread:
            metronome_thread.join()
        if recording_thread:
            recording_thread.join()
        print("\nOperation interrupted by user.")

    print("Program completed.")

# Run the program
if __name__ == "__main__":
    start_program()
