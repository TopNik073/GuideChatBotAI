from DB.user import User
from GigaChat.prompts import Prompts


class ContextManager(Prompts):
    def __init__(self, user: User):
        self.user = user

        super().__init__()

    def add_message(self, role, text):
        message = {"role": role, "content": text}

        if len(self.user.context) == 0:
            self.user.context.append(self.get_start_prompt())
            self.user.context.append(self.get_start_bot_answer())

        if role == "user":
            self.user.context.append(message)

        elif role == "assistant":
            self.user.context.append(message)

        self.user.update()

    def check_is_request(self) -> bool:
        pass
