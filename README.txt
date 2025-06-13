# Simple Voice-Controlled Video Editing Script

## Overview
This project provides a Python script (`video_editor.py`) that allows users to edit videos using voice commands. Users input a video URL (YouTube or direct MP4), record a voice command (e.g., "cut from 10 to 20 seconds"), and the script processes the command to edit the video, saving the result as a new MP4 file. The script uses `moviepy` for video editing, `yt-dlp` for downloading videos, and the Hugging Face API for speech-to-text transcription.

## Project Structure
- **`video_editor.py`**: The main script that:
  - Downloads a video from a YouTube or direct MP4 URL.
  - Records a 5-second audio command via microphone.
  - Transcribes the audio using Hugging Face's `wav2vec2-base-960h` model.
  - Parses the command to extract time codes (e.g., start and end times for cutting).
  - Edits the video using `moviepy` and saves the output.
- **`test_moviepy.py`**: A test script to verify that `moviepy` is correctly installed and can import `VideoFileClip`.
- **`test_transcribe.py`** (optional): A test script to debug the Hugging Face API transcription process.
- **`README.txt`**: This file, providing setup and usage instructions.

## Prerequisites
To run the project, you need:
- **Python 3.12**: The script is tested with Python 3.12.0.
- **FFmpeg**: Required for video processing with `moviepy`.
- **Hugging Face API Token**: Needed for audio transcription via the Hugging Face API.
- **Microphone**: For recording voice commands.
- **Internet Connection**: For downloading videos and accessing the Hugging Face API.

## Setup Instructions

### 1. Install Python 3.12
- Download and install Python 3.12 from [python.org](https://www.python.org/downloads/).
- Ensure "Add Python to PATH" is checked during installation.
- Verify:
  ```bash
  python --version
  ```
  Expected: `Python 3.12.0`.

### 2. Install FFmpeg
- Download FFmpeg from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (e.g., `ffmpeg-7.1.1-essentials_build`).
- Extract to `C:\Users\<your_username>\Downloads\ffmpeg-7.1.1-essentials_build`.
- Add FFmpeg to PATH or specify its path in `video_editor.py`:
  ```python
  os.environ["IMAGEIO_FFMPEG_EXE"] = "/c/Users/<your_username>/Downloads/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe"
  ```
- Verify:
  ```bash
  ffmpeg -version
  ```

### 3. Create a Virtual Environment
- Navigate to your project directory (e.g., `~/Downloads`):
  ```bash
  cd ~/Downloads
  ```
- Create a virtual environment named `video_env`:
  ```bash
  python -m venv video_env
  ```
- Activate the virtual environment (in Git Bash):
  ```bash
  source video_env/Scripts/activate
  ```
  Your prompt should show `(video_env)`.

### 4. Install Dependencies
- In the activated virtual environment, install required packages:
  ```bash
  pip install moviepy==2.2.1 yt-dlp requests sounddevice scipy numpy transformers imageio imageio_ffmpeg torch --no-cache-dir
  ```
- Verify:
  ```bash
  pip list
  ```
  Ensure `moviepy`, `yt-dlp`, `requests`, `sounddevice`, `scipy`, `numpy`, `transformers`, `imageio`, `imageio_ffmpeg`, and `torch` are listed.

### 5. Obtain a Hugging Face API Token
- Sign in to [Hugging Face](https://huggingface.co/settings/tokens).
- Create a new token with Read or Write access.
- Update `video_editor.py` with your token:
  ```python
  API_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  ```

### 6. Verify `moviepy` Installation
- Run the test script:
  ```bash
  python test_moviepy.py
  ```
  Expected output: `VideoFileClip imported successfully!`

## Usage
1. Run the main script:
   ```bash
   python video_editor.py
   ```
2. Enter a video URL (YouTube or direct MP4, e.g., `https://www.youtube.com/watch?v=c-T30NAhJE0` or `https://archive.org/download/sample-video/samplevideo_1280x720_1mb.mp4`).
3. Enter an output video name (without `.mp4` extension, e.g., `output`).
4. Record a 5-second voice command (e.g., say "cut from 10 to 20 seconds").
5. The script will:
   - Download the video.
   - Transcribe the audio command.
   - Cut the video segment.
   - Save the result as `<output_name>.mp4`.
   - Clean up temporary files (`input_video.mp4`, `command.wav`).

## Troubleshooting
- **ModuleNotFoundError**: Ensure all dependencies are installed in the virtual environment.
- **JSON Parsing Error in Transcription**:
  - Verify your Hugging Face API token.
  - Test the API with `test_transcribe.py`:
    ```bash
    python test_transcribe.py
    ```
- **YouTube Download Fails**: Ensure `yt-dlp` is installed and the URL is valid.
- **FFmpeg Errors**: Confirm FFmpeg is accessible via `ffmpeg -version` or the path in `video_editor.py`.
- **PyTorch/TensorFlow Warning**: Ensure `torch` is installed:
  ```bash
  python -c "import torch; print(torch.__version__)"
  ```

## Notes
- The script uses `moviepy` 2.2.1, which imports `VideoFileClip` directly (`from moviepy.video.io.VideoFileClip import VideoFileClip`) instead of the older `moviepy.editor`.
- For local transcription (avoiding the API), modify `transcribe_audio` to use a local `transformers` pipeline (see code comments in `video_editor.py`).
- If `moviepy` issues persist, consider using `ffmpeg-python` as an alternative (requires code changes).