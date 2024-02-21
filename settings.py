import os
from dotenv import load_dotenv
from pydantic import BaseConfig, SecretStr, StrictStr

load_dotenv()

class SiteSettings(BaseConfig):
    api_key: SecretStr = os.getenv('SITE_API_KEY', None)
    api_host: StrictStr = os.getenv('SITE_API_HOST', None)
    
class TelegramSettings(BaseConfig):
    TG_api_key: SecretStr = os.getenv('TG_API_KEY', None)