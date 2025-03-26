from app.application.training.model_trainer import ModelTrainer


config_path = "config.yml"
domain_path = "domain.yml"
training_data_dir = "data"


trainer = ModelTrainer(config_path, domain_path, training_data_dir)
trainer.train(output_dir="models")
