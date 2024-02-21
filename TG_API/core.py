from settings import TelegramSettings
from TG_API.utils.tg_api_handler import TelegramInterface


TG = TelegramSettings()
tg_api = TelegramInterface()

if __name__ == "__main__":
    tg_api()

