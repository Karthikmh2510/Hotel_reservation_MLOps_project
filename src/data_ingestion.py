import os
import pandas as pd
from sklearn.model_selection import train_test_split
from google.cloud import storage
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml

# Initialize logger
logger = get_logger(__name__)

# Creating a class for data ingestion
class DataIngestion:
    def __init__(self, config):

        # Read all variables from config file
        self.config = config["data_ingestion"] # To read the data ingestion part from config file
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        # Storing all raw files in the artifacts/raw directory
        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(f"Data ingestion is started with {self.bucket_name} bucket and {self.file_name} file.")

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name) # File naeme in the bucket
            blob.download_to_filename(RAW_FILE_PATH)  # Download the file to the local path
            
            logger.info(f"File {self.file_name} downloaded from bucket {self.bucket_name} to {RAW_FILE_PATH}.")

        except Exception as e:
            logger.error(f"Error downloading file from GCP: {e}")
            raise CustomException("Failed to download file from GCP", e)
        
    def split_data(self):
        try:
            logger.info("Starting data split into train and test sets.")
            # Read the raw data
            data = pd.read_csv(RAW_FILE_PATH)
            logger.info(f"Raw data read successfully with shape: {data.shape}")
            
            # Split the data into train and test sets
            train_data, test_data = train_test_split(data, test_size = 1-self.train_test_ratio, random_state=42)
            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)
            logger.info(f"Data split completed. Train data shape: {train_data.shape}, Test data shape: {test_data.shape}")
        
        except Exception as e:
            logger.error(f"Error while splitting data: {e}")
            raise CustomException("Failed to split data", e)
        
    def run(self):
        try:
            logger.info("Starting data ingestion process.")
            
            # Download the CSV file from GCP and split the data
            self.download_csv_from_gcp()
            logger.info("CSV file downloaded successfully. Proceeding to split the data.")
            
            # Split the data into train and test sets
            self.split_data()
            logger.info("Data ingestion process completed successfully.")
        
        except CustomException as ce:  
            logger.error(f"CustomeException  {str(ce)}")
            
        finally:
            logger.info("Data ingestion process finished.")
    
if __name__ == "__main__":

    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()
        
