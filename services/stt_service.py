from fastapi import HTTPException
from azure.cognitiveservices.speech import SpeechRecognizer, ResultReason
from factories.speech_factory import SpeechFactory
from config import AzureConfig
from .interfaces.stt_interface import STTInterface

class STTService(STTInterface):
    def __init__(self, config: AzureConfig, factory: SpeechFactory):
        self.config = config
        self.factory = factory

    def speech_to_text(self, audio_path: str) -> str:
        speech_config = self.factory.create_speech_config(self.config)
        recognizer = self.factory.create_recognizer(speech_config, audio_path)
        result = recognizer.recognize_once()
        
        if result.reason != ResultReason.RecognizedSpeech:
            raise HTTPException(status_code=400, detail="Không thể nhận diện giọng nói từ audio")
        return result.text