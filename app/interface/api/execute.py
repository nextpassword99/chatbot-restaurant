from chatterbot import ChatBot
from app.core.config import settings


class Execute:
    @staticmethod
    async def start_chatter_bot():
        return ChatBot('MiBot',
                       storage_adapter='chatterbot.storage.SQLStorageAdapter',
                       logic_adapters=['chatterbot.logic.BestMatch'],
                       database=settings.DB_URL)

    @staticmethod
    async def handle_chat_chatter(chatbot: ChatBot, message):
        return chatbot.get_response(message)
