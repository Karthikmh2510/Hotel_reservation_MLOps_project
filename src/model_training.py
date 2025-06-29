import os
import pandas as pd
import joblib
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml, load_data
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from scipy.stats import randint, uniform

import mlflow # To keep track of all the model we train. Withuot this, 
# we cannot track the model and everytime we train, model will overide the previous one.
import mlflow.sklearn


logger = get_logger(__name__)

class ModelTrainer:

    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info("Loading training data...")
            train_df = load_data(self.train_path)

            logger.info("Loading test data...")
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=['booking_status'])
            y_train = train_df['booking_status']
            X_test = test_df.drop(columns=['booking_status'])
            y_test = test_df['booking_status']
            logger.info(f"Training data splitted successfully for training")

            return X_train, y_train, X_test, y_test

        except Exception as e:
            logger.error(f"Error in loading or splitting data: {e}")
            raise CustomException("Failed to load or split data", e)

    def train_lgbm(self, X_train, y_train,):
        try:
            logger.info("Initializing LightGBM model...")

            lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params['random_state'],
                                            force_col_wise=True)

            logger.info("Hyperparamater Tuning...")
            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params['n_iter'],
                cv=self.random_search_params['cv'],
                n_jobs=self.random_search_params['n_jobs'],
                verbose=self.random_search_params['verbose'],
                random_state=self.random_search_params['random_state'],
                scoring=self.random_search_params['scoring']
            )

            logger.info("Starting Hyperparamater Tuning...")
            random_search.fit(X_train, y_train)
            logger.info("Hyperparameter tuning completed successfully.")

            best_lgbm_model = random_search.best_estimator_
            best_params = random_search.best_params_
            logger.info(f"Best parameters are: {best_params}")

            return best_lgbm_model
        
        except Exception as e:
            logger.error(f"Error during model training: {e}")
            raise CustomException("Failed to train model", e)

    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Evaluating model on test data...")
            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')

            logger.info(f"Model evaluation metrics - Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")
            
            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
            }
        
        except Exception as e:
            logger.error(f"Error during model evaluation: {e}")
            raise CustomException("Failed to evaluate model", e)
        
    def save_model(self, model):
        try:
            logger.info(f"Saving model to {self.model_output_path}...")
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            
            # Save the model using joblib
            joblib.dump(model, self.model_output_path)
            logger.info(f"Model saved successfully at {self.model_output_path}")
        
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise CustomException("Failed to save model", e)
        
    def run(self):
        try:
            with mlflow.start_run():
                logger.info("MLflow run started for model training.")
                logger.info("Logging the training ans testing data to MLflow...")
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                logger.info("Starting model training process...")
                X_train, y_train, X_test, y_test = self.load_and_split_data()
                best_lgbm_model = self.train_lgbm(X_train, y_train)
                evaluation_metrics = self.evaluate_model(best_lgbm_model, X_test, y_test)
                self.save_model(best_lgbm_model)

                logger.info("Logging the model and evaluation metrics to MLflow...")
                mlflow.log_artifact(self.model_output_path)
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(evaluation_metrics)

                logger.info("Model training process completed successfully.")
            
        
        except Exception as e:
            logger.error(f"Error in model training process: {e}")
            raise CustomException("Model training process failed", e)
        
if __name__ == "__main__":
    try:
        logger.info("Starting the model training script...")
        trainer = ModelTrainer(
            train_path=PROCESSED_TRAIN_DATA_PATH,
            test_path=PROCESSED_TEST_DATA_PATH,
            model_output_path=MODEL_FILE_PATH
        )
        evaluation_results = trainer.run()
        logger.info(f"Model evaluation results: {evaluation_results}")
    except Exception as e:
        logger.error(f"An error occurred during model training: {e}")
        raise CustomException("Model training script failed", e)