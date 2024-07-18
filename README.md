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
Open your browser and navigate to http://localhost:8000/docs to explore the interactive API documentation provided by Swagger UI.

## API Endpoints
- POST /vad_check/: Accepts an audio file and indicates if speech detected and returns segments of detected speech.
  - Request: multipart/form-data with an audio file.
  - Response: JSON with boolean to tell if audio has speech and timestamps of detected speech segments.
