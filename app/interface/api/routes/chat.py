from fastapi import APIRouter, Depends
from app.interface.api.schemas import ChatResponseSchema, ChatRequestSchema
from app.interface.api.execute import Execute

router = APIRouter()
agent_instance = None


@router.post("/chat", response_model=ChatResponseSchema)
async def handle_chat_message(
    chat_message: ChatRequestSchema,
):
    global agent_instance
    try:
        if agent_instance is None:
            agent_instance = Execute.get_model(chat_message.model)

        chatbot_response = await agent_instance.handle_text(chat_message.message)
        res = agent_instance.justResponse(chatbot_response)

        return ChatResponseSchema(response=res)
    except:
        return ChatResponseSchema(response="Error")
