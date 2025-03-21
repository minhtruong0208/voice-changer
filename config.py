# config.py
from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class AzureConfig:
    subscription_key: str = os.getenv("AZURE_SUBSCRIPTION_KEY", "default_key")
    region: str = os.getenv("AZURE_REGION", "westus")
    default_voice: str = os.getenv("DEFAULT_VOICE", "vi-VN-HoaiMyNeural")

CONFIG = AzureConfig()

if not CONFIG.subscription_key or CONFIG.subscription_key == "default_key":
    raise ValueError("AZURE_SUBSCRIPTION_KEY không được cấu hình trong .env")