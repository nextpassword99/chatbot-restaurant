from app.application.models.rasa import RasaModel
from app.application.models.chatterbot import ChatterBot
from app.application.models.gemma import GemmaModel
from app.application.models.deepseek import DeepSeekModel
from app.application.models.gemma2 import Gemma2


class Execute:
    @staticmethod
    def get_model(model) -> RasaModel | ChatterBot | GemmaModel | DeepSeekModel | Gemma2 | None:
        if model == "rasa":
            return RasaModel()

        if model == "chatterbot":
            return ChatterBot()

        if model == "gemma":
            return GemmaModel()

        if model == "deepseek":
            return DeepSeekModel()

        if model == "gemma2":
            return Gemma2()
