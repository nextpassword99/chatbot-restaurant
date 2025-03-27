from rasa.core.agent import Agent
from app.core.config import settings


class Rasa:
    def __init__(self):
        self.agent: Agent = self.load_model()

    async def load_model():
        return Agent.load(settings.MODEL_SELECTED)

    async def handle_text(self, msg):
        return await self.agent.handle_text(msg)
