from fastapi import FastAPI, UploadFile, File, HTTPException
from contextlib import asynccontextmanager  # Thêm import này
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

# Định nghĩa lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code chạy khi khởi động (startup) có thể đặt ở đây (nếu cần)
    yield  # Phần giữa yield là khi ứng dụng đang chạy
    # Code chạy khi tắt ứng dụng (shutdown)
    audio_service.cleanup()

# Khởi tạo ứng dụng với lifespan
app = FastAPI(lifespan=lifespan)

@app.post("/voice-changer/")
async def voice_changer(audio: UploadFile = File(None), text: str = None):
    """
    Endpoint chuyển đổi giọng nói:
    - Nếu cung cấp audio, dùng STT để lấy văn bản, rồi TTS để tạo audio.
    - Nếu cung cấp text, dùng trực tiếp TTS để tạo audio.
    """
    if not audio and not text:
        raise HTTPException(status_code=400, detail="Phải cung cấp ít nhất một trong hai: audio hoặc text")
    
    # Xử lý đầu vào
    if audio:
        audio_path = audio_service.save_audio(await audio.read())
        text = stt_service.speech_to_text(audio_path)
    
    # Chuyển văn bản thành audio
    tts_service.text_to_speech(text, CONFIG.output_audio_path)
    
    # Trả file audio
    return audio_service.get_audio_response()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)