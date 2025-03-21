from azure.cognitiveservices.speech import ResultReason
from fastapi import HTTPException
from factories.speech_factory import SpeechFactory
from config import AzureConfig

class STTService:
    def __init__(self, config: AzureConfig, factory: SpeechFactory):
        self.config = config
        self.factory = factory

    def speech_to_text(self, audio_file_path: str) -> str:
        speech_config = self.factory.create_speech_config(self.config)
        recognizer = self.factory.create_recognizer(speech_config, audio_file_path)
        result = recognizer.recognize_once()
        
        if result.reason != ResultReason.RecognizedSpeech:
            raise HTTPException(status_code=400, detail="Không thể nhận diện giọng nói từ audio")
        return result.text