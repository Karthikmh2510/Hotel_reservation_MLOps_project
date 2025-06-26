import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

# Initialize logger
logger = get_logger(__name__)

class DataPreprocessor:

    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir

        self.config= read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
            logger.info(f"Created directory: {self.processed_dir}")
        else:
            logger.info(f"Directory already exists: {self.processed_dir}")

    def prepreprocess_data(self, df):
        try:
            logger.info("Starting data preprocessing...")

            logger.info("Dropping teh columns")
            df.drop(columns=['Booking_ID'], inplace=True, errors='ignore')
            df.drop_duplicates(inplace=True)
            logger.info(f"Dropped duplicates")

            cat_cols = self.config['data_processing']['categorical_columns']
            num_cols = self.config['data_processing']['numerical_columns']

            logger.info("Applying Label Encoding")
            label_encoder = LabelEncoder()
            mappings={}
            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {label:code for label,code in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))}
            logger.info("Label Encoding applied successfully")
            logger.info("Label Mappings are: ")
            for col, mapping in mappings.items():
                logger.info(f"{col}: {mapping}")

            logger.info("Handling Skewness")
            skew_threshold = self.config['data_processing']['skewness_threshold']

            skewness = df[num_cols].apply(lambda x:x.skew())

            for colum in skewness[skewness > skew_threshold].index:
                df[colum] = np.log1p(df[colum])
            
            return df
            
        except Exception as e:
            logger.error(f"Error during preprocessing steps: {e}")
            raise CustomException("Data preprocessing failed", e)

    def balanced_data(self, df):
        try:
            logger.info("Starting data balancing...")
            X = df.drop(columns=['booking_status'])
            y = df['booking_status']

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df['booking_status'] = y_resampled
        
            logger.info("Data balancing completed successfully")
            return balanced_df
        
        except Exception as e:
            logger.error(f"Error during data balancing step: {e}")
            raise CustomException("Data balancing failed", e)
        
    def select_features(self, df):
        try:
            logger.info("Starting feature selection...")
            X = df.drop(columns=['booking_status'])
            y = df['booking_status']

            model = RandomForestRegressor(random_state=42)
            model.fit(X, y)

            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                'Feature': X.columns,
                'Importance': feature_importance
                })
            top_important_features_df = feature_importance_df.sort_values(by='Importance', ascending=False)
            num_features_to_select = self.config['data_processing']['no_of_features']

            top_10_features = top_important_features_df['Feature'].head(num_features_to_select).values
            top_10_df = df[top_10_features.tolist() + ['booking_status']].copy()
            
            logger.info("Selected top features based on importance")
            logger.info("Selected features: {selected_features}")
            
            return top_10_df
        
        except Exception as e:
            logger.error(f"Error during feature selection step: {e}")
            raise CustomException("Feature selection failed", e)
        
    def save_data(self, df, file_path):
        try:
            logger.info(f"Saving data to: {file_path}")
            df.to_csv(file_path, index=False)
            logger.info(f"Data saved successfully at: {file_path}")
            
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            raise CustomException("Failed to save data", e)
        
    def process(self):
        try:
            logger.info("Loading the dat afrom RAW directory")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)
            logger.info("Data loaded successfully")

            train_df = self.prepreprocess_data(train_df)
            test_df = self.prepreprocess_data(test_df)
            logger.info("Preprocessing completed successfully")

            train_df = self.balanced_data(train_df)
            test_df = self.balanced_data(test_df)
            logger.info("Data balancing completed successfully")

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]
            logger.info("Feature selection completed successfully")

            self.save_data(train_df, os.path.join(self.processed_dir, 'processed_train.csv'))
            self.save_data(test_df, os.path.join(self.processed_dir, 'processed_test.csv'))
            logger.info("Data processing completed successfully")

        except Exception as e:
            logger.error(f"Error during data processing: {e}")
            raise CustomException("Data processing failed", e)

if __name__ == "__main__":
    processor = DataPreprocessor(
        train_path=TRAIN_FILE_PATH,
        test_path=TEST_FILE_PATH,
        processed_dir=PROCESSED_DIR,
        config_path=CONFIG_PATH
    )
    processor.process()