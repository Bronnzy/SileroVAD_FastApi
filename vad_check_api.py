import torch
from silero_vad import get_speech_timestamps, load_silero_vad
from silero_vad.utils_vad import (
    read_audio,
    get_speech_timestamps,
)

from typing import Union, Annotated
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, PositiveInt, PositiveFloat

app = FastAPI()

class TimeStamps(BaseModel):
    start: PositiveFloat = 0
    end: PositiveFloat = 0

class Response(BaseModel):
    has_voice: bool
    speech_timestamps: list[TimeStamps] = [TimeStamps()]

@app.post("/vad_check/")
async def vad_check(file: UploadFile) -> Response:
    
    has_voice = False
    model = load_silero_vad()

    audio_path = file.file
    wav = read_audio(audio_path)

    speech_timestamps = get_speech_timestamps(wav, model, return_seconds=True)

    has_voice = bool(speech_timestamps)
    
    print(has_voice)

    response = Response(has_voice=has_voice, speech_timestamps=speech_timestamps)
    return response
