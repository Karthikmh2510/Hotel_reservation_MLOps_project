import os
from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataPreprocessor 
from src.model_training import ModelTrainer
from utils.common_functions import read_yaml
from config.paths_config import *


if __name__ == "__main__":

    # Data Ingestion pipeline
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()

    # Data Preprocessing pipeline
    processor = DataPreprocessor(
        train_path=TRAIN_FILE_PATH,
        test_path=TEST_FILE_PATH,
        processed_dir=PROCESSED_DIR,
        config_path=CONFIG_PATH
    )
    processor.process()

    # Model Training pipeline
    trainer = ModelTrainer(
            train_path=PROCESSED_TRAIN_DATA_PATH,
            test_path=PROCESSED_TEST_DATA_PATH,
            model_output_path=MODEL_FILE_PATH
        )
    trainer.run()