""" import ollama
response = ollama.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content']) """




 
from Whisper import record_audio
from Whisper import transcribe_audio

def whisper():
    # Set the duration of the recording in seconds
    duration = 5  # Adjust this as needed

    # Step 1: Record from the microphone and get the .wav file name
    audio_file = record_audio(duration)

    # Step 2: Transcribe the recorded audio and get the .txt file name
    transcription_file = transcribe_audio(audio_file)

    # Step 3: Print the file names (for reference)
    print("Audio file:", audio_file)
    print("Transcription file:", transcription_file)
    return audio_file, transcription_file

audio_transc = whisper()

audiowav = audio_transc[0]
transcFilename = audio_transc[1]





# return proportion of duration that is silent
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS

def percent_silent(wavfile):
    [Fs, x] = aIO.read_audio_file(wavfile)                                                                      # Fs = sampling frequency/rate; x = signal (numpy array)
    soundseg = aS.silence_removal(x, Fs, 0.020, 0.020, smooth_window = 1.0, weight = 0.7, plot = False)          # returns list of lists, ie list of segments of sound (ea segment element is a list with segment beginning and segment end)
    
    duration = soundseg[len(soundseg)-1][1]
    print(duration)                                         # 18.06 s

    speechseconds = 0
    for seg in soundseg:
        speechseconds += seg[1] - seg[0]
    print(speechseconds)                                    # 5.98 s

    silentseconds = duration - speechseconds
    print(silentseconds)                                    # 12.08 s

    print(silentseconds/duration)                           # 0.67
    return silentseconds/duration
    
percent_silent(audiowav)





# !! not yet tested with Whisper
from pydub import AudioSegment

def wpm(audio, transcription):                                     # audio is .wav file; transcription is string name for transcription
    audiofile = AudioSegment.from_file(audio)
    ms = len(audiofile)
    sec = AudioSegment.duration_seconds(ms)
    min = sec // 60

    transcript = open(transcription, "r")
    text = transcript.read()
    numwords = len(text.split())
    transcript.close()

    return numwords/min

def rel_speed(wpm):
    if wpm < 120:
        return "slow"
    elif wpm < 150:
        return "average"
    else:
        return "fast"
    
wpm = wpm(audiowav, transcFilename)
print(rel_speed(wpm))