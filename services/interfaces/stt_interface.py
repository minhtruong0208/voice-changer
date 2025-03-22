from abc import ABC, abstractmethod

class TTSInterface(ABC):
    @abstractmethod
    def text_to_speech(self, text: str, output_path: str) -> None:
        pass