from fastapi import Depends
from app.infrastructure.database.session import DatabaseSession
from app.domain.repositories.order_repository import SQLOrderRepository
from app.domain.services.order_service import OrderService


def get_db():
    db = DatabaseSession("sqlite:///orders.db")
    try:
        yield db.get_session()
    finally:
        db.get_session().close()


def get_order_service(db=Depends(get_db)) -> OrderService:
    repo = SQLOrderRepository(db)
    return OrderService(repo)
