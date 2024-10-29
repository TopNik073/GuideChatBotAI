from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart


from source.utils.logger_settings import logger
from source.database.database_initialisation import db
from source.messages import user_messages
from source.utils.http_request import get_query


router = Router(name="user_handlers")


# cmd /start
@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot) -> None:
    await db.exist_user(user_id=message.chat.id, 
                        firstname=message.chat.first_name,
                        surname=message.chat.last_name, 
                        username=message.chat.username)
    
    text = user_messages.info_start()
    await bot.send_message(chat_id=message.from_user.id,
                           text=text)
    logger.info(f"User {message.from_user.id}: /start")


@router.message()
async def handle_question(message: Message, bot: Bot) -> None:
    # TODO заменить поля запроса, ответа и endpoint на корректные
    query = {'question': message.text}
    logger.debug(f"Request to API: query = {query}")
    r_status, r_json = await get_query(params=query,
                                       endpoint='INPUT ENDPOINT')
    if r_status == 200:
        text = r_json.get('answer')
        await bot.send_message(chat_id=message.from_user.id,
                               text=text)
        logger.info(f"Success request to API: {r_json}")
    
    
    
    

        
