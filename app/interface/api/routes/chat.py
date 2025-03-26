from fastapi import APIRouter, Depends
from app.interface.api.schemas import ChatResponseSchema, ChatRequestSchema
from app.domain.services.order_service import OrderService
from app.interface.api.dependencies import get_order_service
from rasa.core.agent import Agent

router = APIRouter()
agent = Agent.load("models/nlu-20250326-125852-elegant-adversary.tar.gz")


@router.post("/chat", response_model=ChatResponseSchema)
async def handle_chat_message(
    chat_message: ChatRequestSchema,
):
    response = await agent.handle_text(chat_message.message)
    chatbot_response = response[0]["text"] if response else "Lo siento, no entendí eso."

    return ChatResponseSchema(response=chatbot_response)
