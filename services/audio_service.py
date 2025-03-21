# services/audio_service.py
import os
from fastapi.responses import FileResponse
from pydub import AudioSegment
from config import AzureConfig

class AudioService:
    def __init__(self, config: AzureConfig):
        self.config = config
        self.audio_dir = "audio"
        self.input_dir = os.path.join(self.audio_dir, "input")
        self.output_dir = os.path.join(self.audio_dir, "output")
        self.temp_wav_path = os.path.join(self.audio_dir, "temp_input.wav")
        
        # Tạo các thư mục nếu chưa tồn tại
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def save_audio(self, audio_content: bytes, original_filename: str) -> str:
        # Lưu file gốc vào audio/input/
        input_path = os.path.join(self.input_dir, original_filename)
        with open(input_path, "wb") as f:
            f.write(audio_content)
        
        # Chuyển MP3 sang WAV nếu cần, lưu vào audio/
        if input_path.endswith(".mp3"):
            audio = AudioSegment.from_mp3(input_path)
            audio.export(self.temp_wav_path, format="wav")
            return self.temp_wav_path
        return input_path

    def convert_to_mp3(self, wav_path: str, output_mp3_path: str) -> None:
        # Chuyển WAV sang MP3
        audio = AudioSegment.from_wav(wav_path)
        audio.export(output_mp3_path, format="mp3")

    def get_audio_response(self, input_filename: str) -> FileResponse:
        # Tạo tên file đầu ra: {tên đầu vào}.out.mp3 trong audio/output/
        base_name = os.path.splitext(input_filename)[0]
        output_mp3_path = os.path.join(self.output_dir, f"{base_name}.out.mp3")
        self.convert_to_mp3(self.temp_wav_path, output_mp3_path)
        return FileResponse(output_mp3_path, media_type="audio/mp3", filename=os.path.basename(output_mp3_path))

    def cleanup(self) -> None:
        # Xóa file tạm trong audio/
        if os.path.exists(self.temp_wav_path):
            os.remove(self.temp_wav_path)