from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from .config import Settings
from .handlers import router


# Создаём объекты Bot, Dispatcher, Router, для запуска телеграм-бота.
bot = Bot(token=Settings.TELEGRAM_API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)
