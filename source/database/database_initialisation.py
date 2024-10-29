import asyncio
from .db_model import DataBase
from source.utils.logger_settings import logger
from source.config import DatabaseConfig

db = None

async def init_database():
    global db
    db_config = DatabaseConfig()
    db = DataBase(db_config)
    
    while True:
        try:
            logger.debug('Try connect to Database..')
            await db.create()  # Инициализируем базу данных
            logger.info('Connect to Database was successful!')
            break
        except Exception as e:
            logger.error(f'Failed to connect to Database. Error: {e}')
            logger.info('Retrying in 5 seconds...')
            await asyncio.sleep(5)
