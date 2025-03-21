import os
from fastapi.responses import FileResponse
from config import AzureConfig

class AudioService:
    def __init__(self, config: AzureConfig):
        self.config = config

    def save_audio(self, audio_content: bytes) -> str:
        with open(self.config.input_audio_path, "wb") as f:
            f.write(audio_content)
        return self.config.input_audio_path

    def get_audio_response(self) -> FileResponse:
        return FileResponse(self.config.output_audio_path, media_type="audio/wav", filename="output_audio.wav")

    def cleanup(self) -> None:
        for path in [self.config.input_audio_path, self.config.output_audio_path]:
            if os.path.exists(path):
                os.remove(path)