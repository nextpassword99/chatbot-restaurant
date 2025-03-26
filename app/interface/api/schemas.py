from pydantic import BaseModel


class OrderCreateSchema(BaseModel):
    items: list
    customer_id: str


class ChatRequestSchema(BaseModel):
    message: str


class ChatResponseSchema(BaseModel):
    response: str
