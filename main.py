import os
from functools import partial

from black.lines import append_leaves
from telegram import Update, ReplyKeyboardRemove
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters, CommandHandler
from dotenv import load_dotenv

from GigaChat.GigaChat import GigaChat
from DB.user import User

from GigaChat.prompts import Prompts

from ui.main_controller import main_controller, get_create_new_trip_btn

load_dotenv()

GG = GigaChat()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("ui/start_image.jpg", "rb") as image_file:
        await context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=image_file,
            caption=Prompts().get_start_bot_answer(True),
            parse_mode="Markdown",
        )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, gg: GigaChat):
    try:
        await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

        user = User(
            update.message.from_user["id"],
            update.message.from_user["first_name"],
            update.message.from_user["last_name"],
            update.message.from_user["username"],
        )

        response = await main_controller(user, gg, update.message.text)

        if response.get("rm") is not None:
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text=response["text"],
                reply_markup=response.get("rm"),
                parse_mode="Markdown",
            )
        else:
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text=response["text"],
                reply_markup=ReplyKeyboardRemove(),
                parse_mode="Markdown",
            )
    except Exception as e:
        print(e)
        await context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Извините, что-то пошло не так",
                reply_markup=get_create_new_trip_btn(),
                parse_mode="Markdown",
            )


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.environ.get("BOT_TOKEN")).build()

    msg_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, partial(message_handler, gg=GG))
    start_handler = CommandHandler("start", start)

    application.add_handler(msg_handler)
    application.add_handler(start_handler)

    application.run_polling()
