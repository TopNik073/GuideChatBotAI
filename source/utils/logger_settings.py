import os
from datetime import datetime
import logging.config

from source.config import Settings


# Установка часового пояса
now = datetime.now()

# Создание папки логов, если её нет
logs_dir = os.path.join(Settings.PROJECT_DIR, "logs")
os.makedirs(logs_dir, exist_ok=True)

file_name = f'{logs_dir}/{now.strftime("%d_%m_%Y_time_%H_%M_%S")}.log'

# Формат логов
log_format = '{asctime} - {name} - {levelname} - {message}'


class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Экранирование символов новой строки и табуляции
        record.msg = str(record.msg).replace('\n', '\\n').replace('\t', '\\t')
        return super().format(record)

logger_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            '()': CustomFormatter,
            'format': log_format,
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': file_name,
            'mode': "w"
        }
    },
    'loggers': {
        'TG_BOT': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}




# Инициализация логгера
logging.config.dictConfig(logger_config)
logger = logging.getLogger('TG_BOT')
