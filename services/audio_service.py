import os
from fastapi.responses import FileResponse
from pydub import AudioSegment
from config import AzureConfig
from .interfaces.audio_interface import AudioInterface

class AudioService(AudioInterface):
    def __init__(self, config: AzureConfig):
        self.config = config
        self.audio_dir = "audio"
        self.input_dir = os.path.join(self.audio_dir, "input")
        self.output_dir = os.path.join(self.audio_dir, "output")
        self.temp_wav_path = os.path.join(self.audio_dir, "temp_input.wav")
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def save_audio(self, audio_content: bytes, original_filename: str) -> str:
        input_path = os.path.join(self.input_dir, original_filename)
        with open(input_path, "wb") as f:
            f.write(audio_content)
        if input_path.endswith(".mp3"):
            audio = AudioSegment.from_mp3(input_path)
            audio.set_channels(1).set_frame_rate(16000).export(self.temp_wav_path, format="wav", codec="pcm_s16le")
            return self.temp_wav_path
        return input_path

    def get_audio_response(self, input_filename: str) -> FileResponse:
        base_name = os.path.splitext(input_filename)[0]
        output_mp3_path = os.path.join(self.output_dir, f"{base_name}.out.mp3")
        audio = AudioSegment.from_wav(self.temp_wav_path)
        audio.export(output_mp3_path, format="mp3")
        return FileResponse(output_mp3_path, media_type="audio/mp3", filename=os.path.basename(output_mp3_path))

    def cleanup(self) -> None:
        if os.path.exists(self.temp_wav_path):
            os.remove(self.temp_wav_path)