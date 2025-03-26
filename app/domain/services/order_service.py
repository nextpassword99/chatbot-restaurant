from typing import Optional
from app.domain.models.order_model import Order
from app.domain.repositories.order_repository import IOrderRepository


class OrderService:
    def __init__(self, repository: IOrderRepository):
        self._repository = repository

    def create_order(self, items: list, customer_id: str) -> Order:
        new_order = Order(items=items, customer_id=customer_id)
        return self._repository.save(new_order)

    def get_order_status(self, order_id: int) -> Optional[str]:
        order = self._repository.get_by_id(order_id)
        return order.status if order else None
