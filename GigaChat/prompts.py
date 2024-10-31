class Prompts:
    def get_start_prompt(self):
        with open("GigaChat/prompts/start_prompt.txt", encoding="utf8") as file:
            start_prompt = file.read()

        start_prompt = {
            "role": "system",
            "content": start_prompt,
        }

        return start_prompt

    def get_start_bot_answer(self):
        with open("GigaChat/prompts/start_bot_answer.txt", encoding="utf8") as file:
            start_bot_answer = file.read()

        start_bot_answer = {
            "role": "assistant",
            "content": start_bot_answer,
        }

        return start_bot_answer
