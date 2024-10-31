from telegram import ReplyKeyboardMarkup, KeyboardButton

from DB.user import User
from GigaChat.GigaChat import GigaChat
from GigaChat.ContextManager import ContextManager

from ui.locale import *


async def main_controller(user: User, GG: GigaChat, text: str):
    try:
        if text == CREATE_NEW_TRIP_TEXT and user.available_trips != 0:
            user.context = []
            user.available_trips -= 1
            user.update()

            return {
                "text": "Отлично, давайте создадим новую поездку!",
                "rm": get_create_new_trip_btn(),
            }

        elif text == CREATE_NEW_TRIP_TEXT and user.available_trips == 0:
            return {
                "text": get_pay_text(),
                "rm": get_pay_btn(),
            }

        elif text == PAY_BTN_TEXT:
            user.available_trips += 1
            user.update()
            return {
                "text": get_on_pay_text(),
            }

        else:
            if user.available_trips == 0:
                return {
                "text": get_pay_text(),
                "rm": get_pay_btn(),
            }
            manager: ContextManager = ContextManager(user)
            manager.add_message("user", text)

            answer = await GG.generate_answer(user.context)

            manager.add_message(answer["role"], answer["content"])

            return {
                "text": answer["content"],
                "rm": get_create_new_trip_btn(),
            }

    except Exception as e:
        print(e)

        return {"text": "Извините, что-то пошло не так", "rm": get_create_new_trip_btn()}

def get_create_new_trip_btn():
    return ReplyKeyboardMarkup(
            [
                [KeyboardButton(text=CREATE_NEW_TRIP_TEXT)],
            ],
            resize_keyboard=True,
        )

def get_pay_btn():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text=PAY_BTN_TEXT)
            ]
        ],
        resize_keyboard=True,
    )

def get_pay_text():
    return """Уважаемый пользователь! 

Ваши запросы исчерпаны. 🛑 Чтобы продолжить создавать уникальные программы туристических поездок по Калининградской области с ТурНейро, просим вас пополнить баланс. 💳✨ 

Получите доступ к новым маршрутам, активностям и интересным местам! 🌊🏰  Оплатите новые запросы и пусть ваши путешествия будут незабываемыми! 

Для пополнения баланса нажмите кнопку "Оплатить" и следуйте инструкциям. 

Спасибо, что выбираете ТурНейро! 🌟"""

def get_on_pay_text():
    return """Оплата выполнена успешно! 🎉 

Давайте начнем создание вашей новой поездки. 🗺✨ 

Снова расскажите нам о ваших предпочтениях к путешествию 😊🗓"""