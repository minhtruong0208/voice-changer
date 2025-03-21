# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from contextlib import asynccontextmanager
from config import CONFIG
from factories.speech_factory import SpeechFactory
from services.stt_service import STTService
from services.tts_service import TTSService
from services.audio_service import AudioService

# Khởi tạo các dependency
speech_factory = SpeechFactory()
stt_service = STTService(CONFIG, speech_factory)
tts_service = TTSService(CONFIG, speech_factory)
audio_service = AudioService(CONFIG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    audio_service.cleanup()

app = FastAPI(lifespan=lifespan)

@app.post("/voice-changer/")
async def voice_changer(audio: UploadFile = File(None), text: str = None, output_name: str = None):
    if not audio and not text:
        raise HTTPException(status_code=400, detail="Phải cung cấp ít nhất một trong hai: audio hoặc text")
    
    # Xử lý đầu vào
    if audio:
        audio_path = audio_service.save_audio(await audio.read(), audio.filename)
        text = stt_service.speech_to_text(audio_path)
    
    # Chuyển văn bản thành audio
    tts_service.text_to_speech(text, audio_service.temp_wav_path)
    
    # Đặt tên file đầu ra
    if audio:
        input_filename = audio.filename
    else:
        input_filename = output_name if output_name else "output.mp3"  # Mặc định là "output.mp3"
    
    return audio_service.get_audio_response(input_filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)