from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement
from app.core.config import settings


def train_bot():
    chatbot = ChatBot(
        'MiBot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=['chatterbot.logic.BestMatch',
                        'chatterbot.logic.MathematicalEvaluation'],
        database_uri=settings.DB_URL,
    )

    trainer = ChatterBotCorpusTrainer(chatbot)

    trainer.train('chatterbot.corpus.english')

    custom_training_data = [
        ("Hola", "Hola, ¿cómo estás?"),
        ("Estoy bien, ¿y tú?", "¡Qué bueno! ¿En qué puedo ayudarte hoy?"),
        ("¿Cómo te llamas?", "Me llamo MiBot, ¿y tú?"),
        ("¡Adiós!", "¡Hasta luego!"),
    ]

    for input_text, response_text in custom_training_data:
        input_statement = Statement(input_text)
        response_statement = Statement(response_text)
        chatbot.learn_response(response_statement, input_statement)

    print("Entrenamiento completado.")
