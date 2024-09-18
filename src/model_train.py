import numpy as np
import pandas as pd
import logging
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
import joblib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def load_data(file_path):
    """
    Load the preprocessed data from the specified file path.
    """
    try:
        logging.info(f"Loading data from {file_path}...")
        data = np.load(file_path, allow_pickle=True).item()  # Ensure proper data loading
        logging.info("Data loaded successfully.")
        return data
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise

def preprocess_data(data):
    """
    Convert categorical features to numerical values and prepare data for model training.
    """
    try:
        logging.info("Preprocessing data...")
        df = pd.DataFrame(data)
        
        # Convert categorical features to numeric
        label_encoder = LabelEncoder()
        df['land_use_encoded'] = label_encoder.fit_transform(df['land_use'])
        
        # Features and target variable
        X = df[['current_emissions', 'land_use_encoded', 'population_density', 'temperature', 'sequestration_potential']].values
        y = df['future_emissions'].values

        logging.info("Data preprocessing completed.")
        return X, y
    except Exception as e:
        logging.error(f"Error during data preprocessing: {e}")
        raise

def train_model(X_train, y_train):
    """
    Train the model using the training data.
    """
    try:
        logging.info("Training the model...")
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        logging.info("Model trained successfully.")
        return model
    except Exception as e:
        logging.error(f"Error during model training: {e}")
        raise

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model using the test data.
    """
    try:
        logging.info("Evaluating the model...")
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        logging.info(f"Model evaluation completed. Mean Squared Error: {mse}")
    except Exception as e:
        logging.error(f"Error during model evaluation: {e}")
        raise

def save_model(model, file_path):
    """
    Save the trained model to a file.
    """
    try:
        logging.info(f"Saving the model to {file_path}...")
        joblib.dump(model, file_path)
        logging.info("Model saved successfully.")
    except Exception as e:
        logging.error(f"Error saving the model: {e}")
        raise

def main():
    # Load data
    data = load_data('data/preprocessed_data.npy')

    # Preprocess data
    X, y = preprocess_data(data)

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    evaluate_model(model, X_test, y_test)

    # Save the model
    save_model(model, 'data/trained_model.pkl')

if __name__ == "__main__":
    main()