from sqlalchemy import create_engine
from app.domain.models.order_model import Base
from app.core.config import settings


engine = create_engine(settings.DB_URL)


Base.metadata.create_all(bind=engine)

print("Base de datos inicializada")
