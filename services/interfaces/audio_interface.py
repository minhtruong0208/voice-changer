from abc import ABC, abstractmethod
from fastapi.responses import FileResponse

class AudioInterface(ABC):
    @abstractmethod
    def save_audio(self, audio_content: bytes, original_filename: str) -> str:
        pass

    @abstractmethod
    def get_audio_response(self, input_filename: str) -> FileResponse:
        pass

    @abstractmethod
    def cleanup(self) -> None:
        pass