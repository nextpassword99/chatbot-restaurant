import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_URL: str = os.getenv("DB_URL", "sqlite:///orders.db")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models")
    TRAINING_DATA_DIR: str = os.getenv("TRAINING_DATA_DIR", "data")
    MODEL_SELECTED = str = os.getenv("MODEL_SELECTED", "model")
    MODEL_GEMMA = str = os.getenv("MODEL_GEMMA", "gemma3:1b")
    MODEL_DEEPSEEK = str = os.getenv("MODEL_DEEPSEEK", "deepseek-r1:1.5b")

    class Config:
        env_file = ".env"


settings = Settings()
