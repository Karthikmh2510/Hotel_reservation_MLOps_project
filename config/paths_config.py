import os

########## CREATING PATH FOR DATA INGESTION ##########

RAW_DIR = "artifacts/raw"  # Directory for raw data
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")  # Path for raw data file
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")  # Path for training data file
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")  # Path for test data file

CONFIG_PATH = "config/config.yaml"  # Path for configuration file

########## DATA PROCESSING ##########

PROCESSED_DIR = "artifacts/processed"  # Directory for processed data
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_train.csv")  # Path for processed training data file
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_test.csv")  # Path for processed test data file   


########## MODEL TRAINING ##########

MODEL_DIR = "artifacts/model/lgbm_model.pkl"  # Directory for model artifacts
MODEL_FILE_PATH = os.path.join(MODEL_DIR, "model.pkl")  # Path for model file