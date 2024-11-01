from telegram import ReplyKeyboardMarkup, KeyboardButton

from DB.user import User
from GigaChat.GigaChat import GigaChat
from GigaChat.ContextManager import ContextManager

from ui.locale import *


async def main_controller(user: User, GG: GigaChat, text: str):
    try:
        if text == CREATE_NEW_TRIP_TEXT:
            user.context = []
            user.available_trips -= 1
            user.update()

            return {
                "text": "Отлично, давайте создадим ваше новое увлекательное путешествие!",
                "rm": get_create_new_trip_btn(),
            }


        else:
            manager: ContextManager = ContextManager(user)
            manager.add_message("user", text)

            answer = await GG.generate_answer(user.context)

            make_additional_request, context = manager.add_message(answer["role"], answer["content"])
            flag_add_request = True
            for i in range(5):
                if make_additional_request:
                    answer = await GG.generate_answer(context)
                    print(answer)
                    make_additional_request, context = manager.add_message(role="assistant", text=answer["content"])

                if not make_additional_request:
                    flag_add_request = False
                    break

            if not flag_add_request:
                return {
                    "text": answer["content"],
                    "rm": get_create_new_trip_btn(),
                }

            else:
                return {
                    "text": get_not_found_text(),
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

def get_not_found_text():
    return """К сожалению, в данный момент мы не можем найти подходящие достопримечательности для вашей программы поездки по Калининградской области. 😔

Если у вас есть конкретные пожелания или вопросы, пожалуйста, сообщите! Мы готовы помочь вам в организации вашего путешествия. 🌍✨

Благодарим за понимание! 🙏"""