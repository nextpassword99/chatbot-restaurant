from app.application.training.model_trainer import ModelTrainer
from app.application.training.chatter_trainer import chatbotTrainer


opt = input('''
            Entrenar: 
            1 - Rasa
            2 - ChatterBot
            ''')

if opt == '1':
    config_path = "config.yml"
    domain_path = "domain.yml"
    training_data_dir = "data"

    trainer = ModelTrainer(config_path, domain_path, training_data_dir)
    trainer.train(output_dir="models")
elif opt == '2':
    trainer = chatbotTrainer()
    trainer.train()

else:
    print("Opcion no valida")
