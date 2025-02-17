from silero_vad import get_speech_timestamps, load_silero_vad
from silero_vad.utils_vad import (
    read_audio,
    get_speech_timestamps,
)
from fastapi import FastAPI, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, PositiveFloat
import io

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_silero_vad()

class TimeStamps(BaseModel):
    start: PositiveFloat = 0
    end: PositiveFloat = 0


class Response(BaseModel):
    has_voice: bool
    speech_timestamps: list[TimeStamps] = [TimeStamps()]


@app.post("/vad_check/")
async def vad_check(request: Request) -> Response:
    """
    Endpoint to check for human voice activity in raw audio/video data from a request body.
    
    Parameters:
    - request: FastAPI Request object containing raw audio/video data.

    Returns:
    - Response: A JSON object indicating if speech was detected and the timestamps of speech segments.
    """
    buffer = await request.body()
    file_like_object = io.BytesIO(buffer)
    audio_path = file_like_object    
    wav = read_audio(audio_path)
    speech_timestamps = get_speech_timestamps(wav, model, return_seconds=True)
    has_voice = bool(speech_timestamps)
    response = Response(has_voice=has_voice, speech_timestamps=speech_timestamps)
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
    model = load_silero_vad()
    audio_path = file.file
    wav = read_audio(audio_path)
    speech_timestamps = get_speech_timestamps(wav, model, return_seconds=True)
    has_voice = bool(speech_timestamps)
    response = Response(has_voice=has_voice, speech_timestamps=speech_timestamps)
    return response
