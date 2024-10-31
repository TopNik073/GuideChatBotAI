from DB.user import User
from DB.attractions import Attractions
from GigaChat.prompts import Prompts

import json


class ContextManager(Prompts):
    def __init__(self, user: User):
        self.user: User = user
        self.attractions: Attractions = Attractions()

        super().__init__()

    def add_message(self, role, text):
        message = {"role": role, "content": text}

        if len(self.user.context) == 0:
            self.user.context.append(self.get_start_prompt())
            self.user.context.append(self.get_start_bot_answer())

        if role == "user":
            self.user.context.append(message)

        elif role == "assistant":
            is_request, words = self.extract_JSON(text)
            if is_request:
                attractions = self.attractions.get_attr_by_cat(words)
                if len(attractions) == 0:
                    message = {
                        "role": "user",
                        "content": "Не найдено мест для этих категорий. Попробуй снова отправить json со списком других категорий",
                    }
                    self.user.context.append(message)
                    self.user.update()
                    return True, self.user.context

                else:
                    self.user.context.append(
                        {
                            "role": "user",
                            "content": json.dumps(attractions),
                        }
                    )
                    self.user.update()
                    return False, self.user.context

            self.user.context.append(message)

        self.user.update()
        return False, self.user.context

    def extract_JSON(self, s: str):
        idx1, idx2 = 0, 0
        flag_1, flag_2 = False, False

        for i in range(len(s)):
            if s[i] == "[" or s[i] == "{":
                idx1 = i
                flag_1 = True
                break

        for i in range(len(s) - 1, 0, -1):
            if s[i] == "]" or s[i] == "}":
                idx2 = i
                flag_2 = True
                break

        return flag_1 and flag_2, self.parse_words(s[idx1:idx2])

    def parse_words(self, s: str):
        words = []
        s += " "
        while True:
            idx1 = s.find('"')

            if idx1 == -1:
                break

            idx2 = s.find('"', idx1 + 1)

            words.append(s[idx1 + 1 : idx2])

            s = s[idx2 + 1 :]

        if len(words) != 0 and words[0] == "categories":
            words = words[1:]

        return words
