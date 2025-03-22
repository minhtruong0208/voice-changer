from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig, SpeechSynthesizer
from config import AzureConfig

class SpeechFactory:
    @staticmethod
    def create_speech_config(config: AzureConfig) -> SpeechConfig:
        speech_config = SpeechConfig(subscription=config.subscription_key, region=config.region)
        speech_config.speech_synthesis_voice_name = config.default_voice
        speech_config.speech_recognition_language = "vi-VN"
        return speech_config

    @staticmethod
    def create_recognizer(speech_config: SpeechConfig, audio_file_path: str) -> SpeechRecognizer:
        audio_config = AudioConfig(filename=audio_file_path)
        return SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    @staticmethod
    def create_synthesizer(speech_config: SpeechConfig, output_path: str) -> SpeechSynthesizer:
        audio_config = AudioConfig(filename=output_path)
        return SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)