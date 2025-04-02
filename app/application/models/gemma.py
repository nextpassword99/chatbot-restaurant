import requests

from app.core.config import settings
from app.application.data.content import Content


class GemmaModel:
    def __init__(self):
        self.model = settings.MODEL_GEMMA
        self.chat: str = ""

    async def load_model(self):
        return self

    async def handle_text(self, msg):
        json_content = {
            "model": self.model,
            "prompt": Content.get_prompt(Content.info(), self.chat, msg),
            "options": {
                "temperature": 0.9,
            },
            "stream": False
        }

        response = requests.post(url="http://localhost:11434/api/generate",
                                 json=json_content).json()
        response_text = self.justResponse(response)
        self.save_chat(msg, response_text)

        return response

    @classmethod
    def justResponse(self, response):
        return response["response"]

    def save_chat(self, msg, response_text):
        content_to_add = f"""cliente: {msg}
                            Chatbot: {response_text}
                            """
        self.chat += content_to_add
