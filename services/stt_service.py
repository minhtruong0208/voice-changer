import logging
from fastapi import HTTPException
from azure.cognitiveservices.speech import ResultReason
from factories.speech_factory import SpeechFactory
from config import AzureConfig
from .interfaces.stt_interface import STTInterface

logging.basicConfig(level=logging.INFO)

class STTService(STTInterface):
    def __init__(self, config: AzureConfig, factory: SpeechFactory):
        self.config = config
        self.factory = factory

    def speech_to_text(self, audio_path: str) -> str:
        speech_config = self.factory.create_speech_config(self.config)
        recognizer = self.factory.create_recognizer(speech_config, audio_path)
        result = recognizer.recognize_once()
        logging.info(f"STT result reason: {result.reason}")
        if result.reason != ResultReason.RecognizedSpeech:
            detail = getattr(result, "no_match_details", "Unknown error")
            logging.error(f"Recognition failed: {result.reason}, Detail: {detail}")
            raise HTTPException(status_code=400, detail=f"Không thể nhận diện giọng nói từ audio: {detail}")
        return result.text