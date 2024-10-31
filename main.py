import os
from functools import partial

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters, CommandHandler
from dotenv import load_dotenv

from GigaChat.GigaChat import GigaChat
from DB.user import User

from ui.main_controller import main_controller

load_dotenv()

GG = GigaChat()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""Добро пожаловать в ТурНейро!
Я ваш персональный гид-помощник для путешествий по Калининграду. Пожалуйста, напишите ваши предпочтения (Пример: Древние замки, Море, Форты). 
От вас лишь нужен ответ на два вопроса:
1.На сколько дней вы посещаете наш замечательный город - Калининград?
2.Какие у вас предпочтения к поездке?""")


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, gg: GigaChat):
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    user = User(update.message.from_user["id"], update.message.from_user["first_name"],
                update.message.from_user["last_name"], update.message.from_user["username"])

    response = main_controller(user, gg, update.message.text)

    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=response["text"],
        reply_markup=response.get("rm"),
        parse_mode="Markdown"
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.environ.get("BOT_TOKEN")).build()

    msg_handler = MessageHandler(filters.ALL, partial(message_handler, gg=GG))
    start_handler = CommandHandler("start", start)

    application.add_handler(msg_handler)
    application.add_handler(start_handler)

    application.run_polling()
