from datetime import datetime
from sqlalchemy import select
import logging

from ..database_models import Users

logger = logging.getLogger(__name__)


class UsersQueries:
    """Методы работы с таблицей users"""

    async def add_user(self, user_id: int, firstname: str, surname: str, username: str):
        """Добавление нового пользователя."""
        async with await self.get_session() as session:
            new_user = Users(firstname=firstname, 
                             surname=surname, 
                             username=username, 
                             user_id=user_id,
                             created_at=datetime.now())
            session.add(new_user)
            await session.commit()

    async def update_user(self, user_id: int, firstname: str, surname: str, username: str):
        """Обновление существующего пользователя."""
        async with await self.get_session() as session:
            # Попробуем найти пользователя по user_id
            user = await session.get(Users, user_id)

            if user is not None:
                # Если пользователь найден, обновляем его поля
                user.firstname = firstname
                user.surname = surname
                user.username = username
                await session.commit()
            else:
                raise ValueError(f"User with id {user_id} not found.")
    
    async def exist_user(self, user_id: int, firstname: str, surname: str, username: str):
        """
        Проверка существования пользователя.  
        Если его не в БД - то добавляется.  
        Если он был, то его данные обновляются  
        Возвращается True, если он был в БД, иначе False
        """
        async with await self.get_session() as session:
            result = await session.execute(select(Users).filter_by(user_id=user_id))
            check = result.scalars().first()
        if check:
            await self.update_user(user_id=user_id, 
                                   firstname=firstname,
                                   surname=surname, 
                                   username=username)
        else:
            await self.add_user(user_id=user_id, 
                                firstname=firstname,
                                surname=surname, 
                                username=username)
        return check

    async def get_info_about_user(self, user_id: int) -> Users:
        """Получение информации о пользователе."""
        async with await self.get_session() as session:
            result = await session.execute(select(Users).filter_by(user_id=user_id))
            user: Users = result.scalars().first()
            return user if user else None