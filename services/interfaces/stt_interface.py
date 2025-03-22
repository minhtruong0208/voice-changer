from abc import ABC, abstractmethod

class STTInterface(ABC):
    @abstractmethod
    def speech_to_text(self, audio_path: str) -> str:
        pass