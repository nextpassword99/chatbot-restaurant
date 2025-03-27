from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot.conversation import Statement
from app.core.config import settings
import spacy


class chatbotTrainer:
    def __init__(self):
        self.nlp = spacy.load("es_core_news_sm")
        self.chatbot = self._initialize_chatbot()

    def _initialize_chatbot(self):
        return ChatBot(
            'RestaurantBot',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'Lo siento, no entendí tu pregunta. ¿Podrías reformularla?',
                    'maximum_similarity_threshold': 0.85
                }
            ],
            database_uri=settings.DB_URL,
            preprocessors=[
                'chatterbot.preprocessors.clean_whitespace',
                'chatterbot.preprocessors.unescape_html'
            ]
        )

    def _preprocess_text(self, text: str) -> str:
        """Limpieza y normalización de texto"""
        doc = self.nlp(
            text.lower())
        tokens = [
            token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return " ".join(tokens)

    def train(self):
        corpus_trainer = ChatterBotCorpusTrainer(self.chatbot)
        corpus_trainer.train('chatterbot.corpus.spanish')

        list_trainer = ListTrainer(self.chatbot)

        custom_data = [
            ("Hola", "¡Bienvenido a El Calamar! ¿En qué puedo ayudarte?"),
            ("Quiero hacer un pedido", "Por supuesto, ¿qué te gustaría ordenar?"),
            ("¿Tienen menú vegetariano?",
             "Sí, ofrecemos 5 opciones vegetarianas en nuestro menú."),
            ("¿Cuál es su especialidad?",
             "Nuestra especialidad es el Pulpo a la Parrilla con salsa de ají."),
            ("¿Hacen delivery?",
             "Sí, entregamos en toda el área metropolitana con un costo adicional de S/5"),
        ]

        variations = [
            ("hola", "hey", "buenas", "saludos"),
            ("pedido", "orden", "comida", "ordenar"),
            ("vegetariano", "vegano", "sin carne"),
            ("especialidad", "recomendación", "mejor plato"),
            ("delivery", "domicilio", "envío", "entrega")
        ]

        for pattern in custom_data:
            for variation in variations[custom_data.index(pattern)]:
                input_text = self._preprocess_text(
                    f"{variation} {pattern[0]}")
                response_text = pattern[1]
                list_trainer.train([input_text, response_text])

        print("Chatbot entrenado")
