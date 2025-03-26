from pydantic import BaseModel


class OrderCreateSchema(BaseModel):
    items: list
    customer_id: str


class OrderResponseSchema(BaseModel):
    id: int
    status: str
    items: list

    class Config:
        orm_mode = True
