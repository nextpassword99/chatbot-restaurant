from chatterbot import ChatBot
from app.core.config import settings
from app.application.models.rasa import RasaModel
from app.application.models.chatterbot import ChatterBot
from app.application.models.gemma import GemmaModel


class Execute:
    @staticmethod
    def get_model(model) -> RasaModel | ChatterBot | GemmaModel | None:
        if model == "rasa":
            return RasaModel()

        if model == "chatterbot":
            return ChatterBot()

        if model == "gemma":
            return GemmaModel()
