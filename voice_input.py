import whisper
import subprocess
import os

model = whisper.load_model("base")

def convert_opus_to_wav(opus_path):
    wav_path = opus_path.replace(".opus", ".wav")
    subprocess.run(
        ["ffmpeg", "-y", "-i", opus_path, wav_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return wav_path

def speech_to_text(audio_path):
    if audio_path.endswith(".opus"):
        audio_path = convert_opus_to_wav(audio_path)

    result = model.transcribe(audio_path)
    return result["text"], result["language"]
