# Silero VAD with FastAPI
This repository contains a robust implementation of Silero Voice Activity Detection (VAD) integrated with FastAPI, providing an efficient and scalable solution for real-time audio processing.

## Features
**Silero VAD Integration**: Utilizes the state-of-the-art Silero VAD for accurate voice activity detection.
**FastAPI Framework**: Leverages FastAPI for a high-performance, asynchronous web framework that's easy to use and ideal for building APIs.

## Getting Started
### Prerequisites
- Python 3.8+
- FastAPI
- Silero VAD

## Installation
1. Clone repository
```
git clone https://github.com/Bronnzy/SileroVAD_FastApi.git
```
2. Install the required packages:
```
pip install -r requirements.txt
```

## Running the application
1. Start the FastAPI server
```
uvicorn vad_check_api:app --host 0.0.0.0 --port 4499
```
2. Access the API documentation:
Open your browser and navigate to http://localhost:4499/docs to explore the interactive API documentation provided by Swagger UI.

## API Endpoints
- POST /vad_check/: Accepts audio/video buffer(blob) and indicates if speech detected and returns segments of detected speech.
  - Request
    - Content-Type: multipart/form-data
    - Body: An audio file (e.g., WAV format) uploaded using a form field named 'file'.
  - Response
    - Content-Type: application/json
    - Body: A JSON object containing:
    - has_voice (bool): Indicates whether any speech was detected in the audio.
    - speech_timestamps (list): A list of objects representing the start and end timestamps (in seconds) of detected speech segments..

- POST /vad_check_file/: Accepts an audio/video file and indicates if speech detected and returns segments of detected speech.
  - Request
    - Content-Type: application/octet-stream
    - Body: Raw binary audio data
  - Response
    - Content-Type: application/json
    - Body: A JSON object containing:
    - has_voice (bool): Indicates whether any speech was detected in the audio.
    - speech_timestamps (list): A list of objects representing the start and end timestamps (in seconds) of detected speech segments
