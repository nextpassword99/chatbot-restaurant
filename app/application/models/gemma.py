import requests

from app.core.config import settings
from app.application.data.content import info


class GemmaModel:
    def __init__(self):
        self.model = settings.MODEL_GEMMA
        self.chat: str = ""

    async def load_model(self):
        return self

    def _get_prompt(self, msg):
        return f"""Información: {info} 
                    Usando la información proporcionada, debes responder 
                    solo usando esos datos. 
                    Historial de conversación: {self.chat}
                    Debes responder a la siguiente pregunta: {msg}. 
                    Debes tener un tono de cordialidad como si estuvieras 
                    atendiendo a una persona. Debe ser una respuesta breve. 
                    Hazlo directo sin añadir otros detalles. Usa íconos.
                    Actúa como si estuvieras atendiendo a una persona.
                    """

    async def handle_text(self, msg):
        json_content = {
            "model": self.model,
            "prompt": self._get_prompt(msg),
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
