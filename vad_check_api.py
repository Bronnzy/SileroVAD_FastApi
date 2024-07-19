from silero_vad import get_speech_timestamps, load_silero_vad
from silero_vad.utils_vad import (
    read_audio,
    get_speech_timestamps,
)
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, PositiveFloat
import io

app = FastAPI()

origins = {"http://localhost", "http://localhost:4499", "*"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TimeStamps(BaseModel):
    start: PositiveFloat = 0
    end: PositiveFloat = 0


class Response(BaseModel):
    has_voice: bool
    speech_timestamps: list[TimeStamps] = [TimeStamps()]


@app.post("/vad_check/")
async def vad_check(request: Request) -> Response:
    buffer = await request.body()
    file_like_object = io.BytesIO(buffer)
    has_voice = False
    model = load_silero_vad()
    audio_path = file_like_object
    wav = read_audio(audio_path)
    speech_timestamps = get_speech_timestamps(wav, model, return_seconds=True)
    has_voice = bool(speech_timestamps)
    response = Response(has_voice=has_voice, speech_timestamps=speech_timestamps)
    return response
