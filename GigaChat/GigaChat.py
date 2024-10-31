import os

import requests
import uuid
import time
import json

from dotenv import load_dotenv
from pyexpat.errors import messages

from DB.user import User


class GigaChat:
    def __init__(self):
        self.access_token: str | None = None
        self.expires_at: int | None = None

    def get_token(self):
        try:
            response = requests.post(
                url="https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
                headers={
                    "Authorization": f'Bearer {os.environ.get("MASTER_TOKEN")}',
                    "RqUID": str(uuid.uuid4()),
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={"scope": "GIGACHAT_API_CORP"},
                verify=False,
                timeout=15.0,
            )

            if response.status_code != 200:
                raise BaseException(f"Can't get access token. Status code {response.status_code}")

            response = response.json()

            self.access_token = response["access_token"]
            self.expires_at = response["expires_at"]

            return

        except Exception as e:
            raise e

    async def generate_answer(self, content):
        try:
            if not self.is_token_valid():
                self.get_token()

            response = requests.post(
                url="https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.access_token}",
                },
                data=json.dumps(
                    {
                        "model": "GigaChat-Pro",
                        "messages": content,
                        "stream": False,
                        "repetition_penalty": 1,
                        "temperature": 0.3,
                        "top_p": 0.1,
                    }
                ),
                verify=False,
                timeout=15.0,
            )

            if response.status_code != 200:
                raise BaseException(f"Can't generate answer. Status code {response.status_code}")

            response = response.json()

            return response["choices"][0]["message"]

        except Exception as e:
            raise e

    def is_token_valid(self) -> bool:
        if self.access_token is not None and int(time.time()) < self.expires_at:
            return True

        return False


if __name__ == "__main__":
    gg = GigaChat()
    cnt = [{"role": "user", "content": "Привет, как твои дела?"}]
    res = gg.generate_answer(cnt)
    print(res)
