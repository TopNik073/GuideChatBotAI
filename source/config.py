from dataclasses import dataclass
from environs import Env
import os
from pathlib import Path


project_dir = Path(__file__).resolve().parent.parent

# Загрузка .env
env_path = os.path.join(project_dir, 'deployments', ".env")

env = Env()
try:
    env.read_env(env_path)
except OSError:
    pass

@dataclass
class DatabaseConfig:
    host: str = env.str("HOST_DB")
    port: str = env.str("PORT_DB")
    user: str = env.str("USER_DB")
    password: str = env.str("PASSWORD_DB")
    database_name: str = env.str("NAME_DB")

    def connection_link(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_name}"

@dataclass
class Settings:
    TELEGRAM_API_TOKEN: str = env.str("TELEGRAM_API_TOKEN")
    ADMIN_ID: int = env.int("ADMIN_ID")
    URL_TO_API: str = env.str("URL_TO_API")
    PROJECT_DIR: Path = project_dir
