from fastapi import HTTPException
from factories.speech_factory import SpeechFactory
from config import AzureConfig

class TTSService:
    def __init__(self, config: AzureConfig, factory: SpeechFactory):
        self.config = config
        self.factory = factory

    def text_to_speech(self, text: str, output_path: str) -> None:
        speech_config = self.factory.create_speech_config(self.config)
        synthesizer = self.factory.create_synthesizer(speech_config, output_path)
        synthesis_result = synthesizer.speak_text_async(text).get()
        
        if synthesis_result.reason != synthesis_result.SynthesisCompleted:
            raise HTTPException(status_code=500, detail="Không thể tạo audio đầu ra")