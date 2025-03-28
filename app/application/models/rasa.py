from rasa.core.agent import Agent
from app.core.config import settings
from typing import Optional


class RasaModel:
    _agent: Optional[Agent] = None

    @classmethod
    async def load_agent(cls):
        if cls._agent is None:
            cls._agent = Agent.load(settings.MODEL_SELECTED)
        return cls._agent

    @classmethod
    async def handle_text(cls, text: str, sender_id: str = "default"):
        if cls._agent is None:
            await cls.load_agent()
        return await cls._agent.handle_text(text, sender_id=sender_id)

    @classmethod
    def justResponse(cls, res):
        return res[0]['text']
