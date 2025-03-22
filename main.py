from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from contextlib import asynccontextmanager
from config import CONFIG
from factories.speech_factory import SpeechFactory
from services.stt_service import STTService
from services.tts_service import TTSService
from services.audio_service import AudioService
from services.voice_changer_service import VoiceChangerService

# Khởi tạo dependencies
speech_factory = SpeechFactory()
stt_service = STTService(CONFIG, speech_factory)
tts_service = TTSService(CONFIG, speech_factory)
audio_service = AudioService(CONFIG)
voice_changer_service = VoiceChangerService(stt_service, tts_service, audio_service)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    audio_service.cleanup()

app = FastAPI(lifespan=lifespan)

@app.post("/voice-changer/")
async def voice_changer(
    audio: UploadFile = File(None),
    text: str = Form(None),
    output_name: str = Form(None)
):
    audio_content = await audio.read() if audio else None
    audio_filename = audio.filename if audio else None
    return await voice_changer_service.process(audio_content, audio_filename, text, output_name)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)