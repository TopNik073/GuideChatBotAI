from asyncio import current_task
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session, AsyncEngine, AsyncSession

from .tables import UsersQueries

class DataBase(UsersQueries):
    def __init__(self, config):
        self.config = config
        self.engine: AsyncEngine | None = None
        self.session_maker = None
        self.scoped_session = None

    async def create(self):
        """Создаем движок и сессию для асинхронной работы с базой данных."""
        self.engine = AsyncEngine(create_engine(
            url=self.config.connection_link(),
            echo=False,
            pool_size=20,
            max_overflow=20,
            pool_recycle=3600,
            pool_pre_ping=True,
            future=True
            )
        )
        # Создаем все таблицы
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        # Создаем фабрику сессий и scoped session
        self.session_maker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        self.scoped_session = async_scoped_session(
            self.session_maker,
            scopefunc=current_task
        )

    async def close(self):
        """Закрываем движок базы данных."""
        if self.engine is None:
            raise Exception("Database is not initialized")
        await self.engine.dispose()

    async def __aenter__(self):
        """Вход в асинхронный контекст (инициализация сессии)."""
        if self.scoped_session is None:
            raise Exception("Database is not initialized")
        self.session = self.scoped_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Выход из асинхронного контекста (закрытие сессии)."""
        await self.session.close()

    async def get_session(self):
        """Возвращаем асинхронную сессию."""
        if self.scoped_session is None:
            raise Exception("Database is not initialized")
        return self.scoped_session()
