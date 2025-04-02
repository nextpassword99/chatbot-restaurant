import requests
from app.core.config import settings


class GemmaModel:
    def __init__(self):
        self.model = settings.MODEL_GEMMA

    async def load_model(self):
        return self

    async def handle_text(self, msg):
        json_content = {
            "model": self.model,
            "prompt": msg,
            "stream": False
        }

        return requests.post(url="http://localhost:11434/api/generate",
                             json=json_content).json()

    @classmethod
    def justResponse(self, response):
        return response["response"]
