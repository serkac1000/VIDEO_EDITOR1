import os
import requests
from moviepy.video.io.VideoFileClip import VideoFileClip
import sounddevice as sd
import scipy.io.wavfile as wavfile
import numpy as np
import re
from transformers import pipeline
import yt_dlp

API_TOKEN = "hf_QDPvjMJZqKKXqRyEHggXMFPDmVTBQELf"  # Replace with your Hugging Face token
API_URL = "https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def download_video(url, filename="input_video.mp4"):
    """Download video from the provided URL using yt-dlp."""
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': filename,
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return filename
    except Exception as e:
        raise Exception(f"Failed to download video: {e}")

def record_audio(duration=5, samplerate=16000):
    """Record audio for the specified duration and save as WAV."""
    print(f"Recording audio for {duration} seconds...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    wavfile.write("command.wav", samplerate, recording)
    return "command.wav"

def transcribe_audio(audio_file):
    """Transcribe audio using Hugging Face API."""
    with open(audio_file, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    result = response.json()
    if "text" in result:
        return result["text"].lower()
    else:
        raise Exception("Transcription failed: " + str(result))

def parse_time_codes(command):
    """Parse time codes from voice command (e.g., 'cut from 10 to 20 seconds')."""
    pattern = r"cut from (\d+) to (\d+) seconds"
    match = re.search(pattern, command)
    if match:
        start_time = int(match.group(1))
        end_time = int(match.group(2))
        if start_time < end_time:
            return start_time, end_time
    return None, None

def edit_video(input_video, start_time, end_time, output_name):
    """Cut video segment and save as new MP4 file."""
    video = VideoFileClip(input_video)
    if start_time is None or end_time is None or end_time > video.duration:
        print("Invalid time codes or exceeds video duration.")
        return False
    edited_video = video.subclip(start_time, end_time)
    output_path = output_name if output_name.endswith(".mp4") else output_name + ".mp4"
    edited_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    video.close()
    edited_video.close()
    print(f"Video saved as {output_path}")
    return True

def main():
    video_url = input("Enter the video URL (YouTube or direct MP4): ")
    output_name = input("Enter the output video name (without extension): ")
    try:
        input_video = download_video(video_url)
    except Exception as e:
        print(f"Error downloading video: {e}")
        return
    try:
        audio_file = record_audio(duration=5)
        command = transcribe_audio(audio_file)
        print(f"Transcribed command: {command}")
    except Exception as e:
        print(f"Error with audio processing: {e}")
        return
    start_time, end_time = parse_time_codes(command)
    if start_time is None or end_time is None:
        print("Could not parse time codes. Please say 'cut from X to Y seconds'.")
        return
    try:
        edit_video(input_video, start_time, end_time, output_name)
    except Exception as e:
        print(f"Error editing video: {e}")
    finally:
        if os.path.exists(input_video):
            os.remove(input_video)
        if os.path.exists("command.wav"):
            os.remove("command.wav")

if __name__ == "__main__":
    main()