from fastapi import APIRouter, Depends
from app.interface.api.schemas import ChatResponseSchema, ChatRequestSchema
from rasa.core.agent import Agent
from app.core.config import settings

router = APIRouter()
agent = Agent.load(settings.MODEL_SELECTED)


@router.post("/chat", response_model=ChatResponseSchema)
async def handle_chat_message(
    chat_message: ChatRequestSchema,
):
    response = await agent.handle_text(chat_message.message)
    chatbot_response = response[0]["text"] if response else "Lo siento, no entendí eso."

    return ChatResponseSchema(response=chatbot_response)
