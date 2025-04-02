from chatterbot import ChatBot
from app.core.config import settings
from app.application.models.rasa import RasaModel
from app.application.models.chatterbot import ChatterBot
from app.application.models.gemma import GemmaModel


class Execute:
    @staticmethod
    def get_model(model) -> RasaModel | ChatterBot | GemmaModel | None:
        if model == "rasa":
            return RasaModel()

        if model == "chatterbot":
            return ChatterBot()

        if model == "gemma":
            return GemmaModel()

    @staticmethod
    async def start_chatter_bot():
        return ChatBot('MiBot',
                       storage_adapter='chatterbot.storage.SQLStorageAdapter',
                       logic_adapters=['chatterbot.logic.BestMatch'],
                       database=settings.DB_URL)

    @staticmethod
    async def handle_chat_chatter(chatbot: ChatBot, message):
        return chatbot.get_response(message)
