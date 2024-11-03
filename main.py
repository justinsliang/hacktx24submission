import ollama
from Whisper import record_audio, transcribe_audio
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS
from pydub import AudioSegment


# Step 1: Record and Transcribe Audio
def whisper():
    # Set the duration of the recording in seconds
    duration = 60  # Adjust this as needed

    # Record from the microphone and get the .wav file name
    audio_file = record_audio(duration)

    # Transcribe the recorded audio and get the .txt file name
    transcription_file = transcribe_audio(audio_file)

    # Print the file names for reference
    print("Audio file:", audio_file)
    print("Transcription file:", transcription_file)
    return audio_file, transcription_file

audio_transc = whisper()
audiowav = audio_transc[0]
transcFilename = audio_transc[1]

# Step 2: Analyze Silence in the Audio for Percent Silence
def percent_silent(wavfile):
    [Fs, x] = aIO.read_audio_file(wavfile)
    soundseg = aS.silence_removal(x, Fs, 0.020, 0.020, smooth_window=1.0, weight=0.7, plot=False)

    duration = soundseg[-1][1]
    print(f"Speech duration: {duration}")

    speechseconds = sum(seg[1] - seg[0] for seg in soundseg)
    print(f"Spoke for {speechseconds} seconds")

    silentseconds = duration - speechseconds
    print(f"Silent for {silentseconds} seconds")

    percent_silent = (silentseconds / duration) * 100
    print(f"Silent {percent_silent}% of response.")
    return percent_silent

silence_percentage = percent_silent(audiowav)


# Step 3: Calculate Words Per Minute (WPM)
def wpm(audio, transcription):
    audiofile = AudioSegment.from_file(audio)
    ms = len(audiofile)
    sec = ms / 1000
    minutes = sec / 60

    with open(transcription, "r") as transcript:
        text = transcript.read()
        numwords = len(text.split())

    wpm_value = numwords / minutes if minutes > 0 else 0
    print(f"WPM: {wpm_value}")
    return wpm_value

wpm_value = wpm(audiowav, transcFilename)


# Step 4: Determine Speaking Speed Quality
def rel_speed(wpm):
    if wpm < 120:
        return "slow"
    elif wpm < 150:
        return "average"
    else:
        return "fast"

speed_quality = rel_speed(wpm_value)


# Step 5: Use Ollama to Provide Feedback and Generate Questions
def ollama_feedback_and_questions(wpm_value, speed_quality, transcription_file, job_role):
    # Read transcription text for analysis
    with open(transcription_file, "r") as f:
        transcription_text = f.read()
    
    # Craft the prompt for Ollama based on user's WPM and transcription
    prompt = (
        f"The user spoke at a rate of {wpm_value:.2f} words per minute, which is considered '{speed_quality}' speed.\n"
        f"The transcription of their response is:\n\n\"{transcription_text}\"\n\n"
        f"Based on this transcription, please provide feedback on their speaking speed and the quality of their message. "
        f"Additionally, the user is interested in practicing for an interview for a {job_role} role. "
        f"Please generate 3-5 relevant interview questions for this role."
    )

    # Use Ollama API to generate the response
    response = ollama.chat(model='llama3.2', messages=[
        {'role': 'user', 'content': prompt}
    ])
    
    # Display feedback and interview questions
    print("Ollama's Feedback and Suggested Interview Questions:")
    print(response['message']['content'])

# Example job role for demonstration
job_role = "data analyst"  # Adjust as needed based on user request
ollama_feedback_and_questions(wpm_value, speed_quality, transcFilename, job_role)
