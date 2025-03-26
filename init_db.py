from sqlalchemy import create_engine
from .src.domain.models.order_model import Base
from .src.core.config import settings


engine = create_engine(settings.DB_URL)


Base.metadata.create_all(bind=engine)

print("Base de datos inicializada")
