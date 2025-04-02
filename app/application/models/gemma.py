import requests

from app.core.config import settings
from app.application.data.content import info


class GemmaModel:
    def __init__(self):
        self.model = settings.MODEL_GEMMA

    async def load_model(self):
        return self

    def _get_prompt(self, msg):
        return f"""Información: {info} \n Usando la información proporcionada, debes responder 
                    solo usando esos datos a la siguiente pregunta: {msg}. 
                    Debes tener un tono de cordialidad como si estuvieras 
                    atendiendo a una persona. Debe ser una respuesta breve. 
                    Hazlo directo sin añadir otros detalles"""

    async def handle_text(self, msg):
        json_content = {
            "model": self.model,
            "prompt": self._get_prompt(msg),
            "stream": False
        }

        return requests.post(url="http://localhost:11434/api/generate",
                             json=json_content).json()

    @classmethod
    def justResponse(self, response):
        return response["response"]
