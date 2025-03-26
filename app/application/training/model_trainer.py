from rasa import train
from typing import Optional


class ModelTrainer:
    def __init__(self, config_path: str, domain_path: str, training_data_dir: str):
        self.config_path = config_path
        self.domain_path = domain_path
        self.training_data_dir = training_data_dir

    def train(self, output_dir: str = "models") -> str:
        model_path = train(
            domain=self.domain_path,
            config=self.config_path,
            training_files=self.training_data_dir,
            output=output_dir,
            force_training=True
        )
        return model_path
