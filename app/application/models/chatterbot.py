from chatterbot import ChatBot
from app.core.config import settings


class ChatterBot:
    def __init__(self):
        self.model: ChatBot = self.load_model()

    async def load_model() -> ChatBot:
        return ChatBot(
            'RestaurantBot',
            database_uri=settings.DB_URL,
            read_only=True
        )

    async def handle_text(self, msg):
        return self.model.get_response(msg)
