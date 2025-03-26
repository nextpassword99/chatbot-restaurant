from fastapi import APIRouter, Depends
from .....src.interface.api.schemas import OrderResponseSchema
from .....src.domain.services.order_service import OrderService

router = APIRouter()


@router.post("/chat", response_model=OrderResponseSchema)
async def handle_chat_message(
    message: str,
    order_service: OrderService = Depends(get_order_service)
):
    order = order_service.create_order(
        items=message.split(','),
        customer_id="user123")

    return OrderResponseSchema(id=order.id, status=order.status, items=order.items)
