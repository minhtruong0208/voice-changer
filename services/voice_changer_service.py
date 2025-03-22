from fastapi import HTTPException
from fastapi.responses import FileResponse
import uuid
from .interfaces.stt_interface import STTInterface
from .interfaces.tts_interface import TTSInterface
from .interfaces.audio_interface import AudioInterface

class VoiceChangerService:
    def __init__(self, stt_service: STTInterface, tts_service: TTSInterface, audio_service: AudioInterface):
        self.stt_service = stt_service
        self.tts_service = tts_service
        self.audio_service = audio_service

    async def process(self, audio_content: bytes, audio_filename: str, text: str, output_name: str) -> FileResponse:
        if not audio_content and not text:
            raise HTTPException(status_code=400, detail="Phải cung cấp ít nhất một trong hai: audio hoặc text")
        if audio_content:
            audio_path = self.audio_service.save_audio(audio_content, audio_filename)
            text = self.stt_service.speech_to_text(audio_path)
        self.tts_service.text_to_speech(text, self.audio_service.temp_wav_path)
        input_filename = audio_filename if audio_content else (output_name or f"output_{uuid.uuid4().hex}.mp3")
        return self.audio_service.get_audio_response(input_filename)