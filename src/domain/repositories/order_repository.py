from abc import ABC, abstractmethod
from typing import Optional, List
from ....src.domain.models.order_model import Order


class IOrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def update_status(self, order_id: int, status: str) -> None:
        pass


class SQLOrderRepository(IOrderRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def save(self, order: Order) -> Order:
        with self.session_factory() as session:
            session.add(order)
            session.commit()
            session.refresh(order)
            return order

    def get_by_id(self, order_id: int) -> Optional[Order]:
        with self.session_factory() as session:
            return session.query(Order).filter(Order.id == order_id).first()

    def update_status(self, order_id: int, status: str) -> None:
        with self.session_factory() as session:
            order = session.query(Order).filter(Order.id == order_id).first()
            if order:
                order.status = status
                session.commit()
