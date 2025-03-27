from fastapi import APIRouter, Depends
from app.interface.api.schemas import ChatResponseSchema, ChatRequestSchema
from rasa.core.agent import Agent
from app.core.config import settings
from app.interface.api.execute import Execute

router = APIRouter()


@router.post("/chat", response_model=ChatResponseSchema)
async def handle_chat_message(
    chat_message: ChatRequestSchema,
):
    if chat_message.model == "rasa":
        agent = Agent.load(settings.MODEL_SELECTED)
        response = await agent.handle_text(chat_message.message)
        chatbot_response = response[0]["text"] if response else "Lo siento, no entendí eso."

    if chat_message.model == "chatterbot":
        agent = await Execute.start_chatter_bot()
        chatbot_response = await Execute.handle_chat_chatter(agent, chat_message.message)

    return ChatResponseSchema(response=chatbot_response)
