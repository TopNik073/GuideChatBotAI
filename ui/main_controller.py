from DB.user import User
from GigaChat.GigaChat import GigaChat


def main_controller(user: User, GG: GigaChat, text: str):
    return {"text": text}
