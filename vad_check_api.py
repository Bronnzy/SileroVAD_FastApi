from silero_vad import get_speech_timestamps, load_silero_vad
from silero_vad.utils_vad import (
    read_audio,
    get_speech_timestamps,
)
from fastapi import FastAPI, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, PositiveFloat
import io

# Initialize the FastAPI application
app = FastAPI()

origins = ["*"]

# Configure CORS settings to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the Silero VAD model
model = load_silero_vad()

# Define a Pydantic model for the timestamp data
class TimeStamps(BaseModel):
    start: PositiveFloat = 0    # Start time of speech segment in seconds
    end: PositiveFloat = 0    # End time of speech segment in seconds


# Define a Pydantic model for the API response
class Response(BaseModel):
    has_voice: bool    # Indicates if speech was detected
    speech_timestamps: list[TimeStamps] = [TimeStamps()]    # List of detected speech segments


@app.post("/vad_check/")
async def vad_check(request: Request) -> Response:
    """
    Endpoint to check for human voice activity in raw audio/video data from a request body.
    
    Parameters:
    - request: FastAPI Request object containing raw audio/video data.

    Returns:
    - Response: A JSON object indicating if speech was detected and the timestamps of speech segments.
    """
    buffer = await request.body()    # Retrieve the raw audio data from the request bod
    file_like_object = io.BytesIO(buffer)    # Convert the raw data to a file-like object
    audio_path = file_like_object    
    wav = read_audio(audio_path)    # Read the audio data using the read_audio function
    speech_timestamps = get_speech_timestamps(wav, model, return_seconds=True)    # Detect speech segments
    has_voice = bool(speech_timestamps)    # Determine if any speech was detected
    response = Response(has_voice=has_voice, speech_timestamps=speech_timestamps)    # Create response object
    return response


@app.post("/vad_check_file/")
async def vad_check_file(file: UploadFile) -> Response:
    """
    Endpoint to check for human voice activity in an uploaded audio/video file.

    Parameters:
    - file: FastAPI UploadFile object containing the file.

    Returns:
    - Response: A JSON object indicating if speech was detected and the timestamps of speech segments.
    """
    model = load_silero_vad()    # Load the Silero VAD model (reloading in each request for consistency)
    audio_path = file.file    # Get the file object from the UploadFile
    wav = read_audio(audio_path)    # Read the audio data using the read_audio function
    speech_timestamps = get_speech_timestamps(wav, model, return_seconds=True)    # Detect speech segments
    has_voice = bool(speech_timestamps)    # Determine if any speech was detected
    response = Response(has_voice=has_voice, speech_timestamps=speech_timestamps)    # Create response object
    return response
