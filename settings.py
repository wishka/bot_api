import os
from dotenv import load_dotenv
from pydantic import BaseConfig, SecretStr, StrictStr

load_dotenv()


class SiteSettings(BaseConfig):
    api_key: SecretStr = os.getenv('SITE_API_KEY', None)
    
    
class TelegramSettings(BaseConfig):
    TG_api_key: SecretStr = os.getenv('TG_API_KEY', None)
    TG_admin_id: SecretStr = os.getenv('ADMIN_ID', None)