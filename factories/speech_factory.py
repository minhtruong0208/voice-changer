# factories/speech_factory.py
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig, SpeechSynthesizer

class SpeechFactory:
    @staticmethod
    def create_speech_config(config: "AzureConfig") -> SpeechConfig:
        speech_config = SpeechConfig(subscription=config.subscription_key, region=config.region)
        speech_config.speech_synthesis_voice_name = config.default_voice
        return speech_config

    @staticmethod
    def create_recognizer(speech_config: SpeechConfig, audio_file_path: str) -> SpeechRecognizer:
        audio_config = AudioConfig(filename=audio_file_path)
        return SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    @staticmethod
    def create_synthesizer(speech_config: SpeechConfig, output_path: str) -> SpeechSynthesizer:
        audio_config = AudioConfig(filename=output_path)  # Dùng AudioConfig cho đầu ra
        return SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)