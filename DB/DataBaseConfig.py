import os
from dotenv import load_dotenv

load_dotenv()


class DataBaseConfig:
    DB_USER = "postgres"
    DB_PASS = os.environ.get("DB_PASS")
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "GuideBot"
    DB_CONN = "psycopg2"
    DB_TYPE = "postgresql"
