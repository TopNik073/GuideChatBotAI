class Prompts:
    def get_start_prompt(self):
        with open("GigaChat/prompts/start_prompt.txt", "r") as file:
            start_prompt = file.read()

        return start_prompt
