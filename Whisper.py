import pyaudio
import wave
import whisper
from datetime import datetime

def record_audio(duration: int) -> str:
    """Records audio from the microphone for a given duration and saves it as a WAV file with a timestamped name."""
    print("Recording started...")
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"audio_{timestamp}.wav"
    
    # Parameters for recording
    fs = 16000  # Sample rate
    channels = 1
    format = pyaudio.paInt16  # 16-bit resolution

    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    
    # Open the stream
    stream = audio.open(format=format, channels=channels, rate=fs, input=True, frames_per_buffer=1024)
    
    frames = []
    
    # Record the audio in chunks
    for _ in range(0, int(fs / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Save the recording as a WAV file
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
    
    print(f"Recording finished. Audio saved as {filename}")
    return filename

def transcribe_audio(file_path: str) -> str:
    """Transcribes the given audio file using Whisper and saves it as a .txt file with a timestamped name."""
    # Generate transcription filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    transcription_filename = f"transcription_{timestamp}.txt"
    
    # Load Whisper model and transcribe
    model = whisper.load_model("tiny")  # Choose model size: "tiny", "base", "small", etc.
    result = model.transcribe(file_path)
    transcription = result["text"]
    
    # Save transcription to a .txt file
    with open(transcription_filename, "w") as f:
        f.write(transcription)
    
    print(f"Transcription finished. Text saved as {transcription_filename}")
    return transcription_filename