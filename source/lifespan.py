from .bot import bot
from .config import Settings
from .utils.logger_settings import logger

async def on_startup():
    logger.info('Bot is online!')
    text = 'Бот запущен!'
    await bot.send_message(chat_id=Settings.ADMIN_ID, text=text)


async def on_shutdown():
    logger.info('Bot is stopped!')
    text = 'Бот остановлен!'
    await bot.send_message(chat_id=Settings.ADMIN_ID, text=text)