import sys
import os
import numpy as np
import joblib
import logging

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from model_train import train_model
from preprocessing import preprocess_data
from optimization import recommend_land_use_changes

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def main():
    logging.info("Fetching GHG Data...")
    from data_fetch import fetch_ghg_data  # Make sure this module is available
    fetch_ghg_data()

    logging.info("Preprocessing data...")
    df = preprocess_data()
    if df is None:
        logging.error("Preprocessing failed.")
        return

    logging.info("Training model...")
    try:
        # Load preprocessed data
        data = np.load('data/preprocessed_data.npy', allow_pickle=True).item()
        X_train = data['X_train']
        y_train = data['y_train']
        
        # Train the model
        model = train_model(X_train, y_train)
        logging.info("Model trained successfully.")

        # Save the model
        model_save_path = 'data/trained_model.pkl'
        joblib.dump(model, model_save_path)
        logging.info(f"Model saved to {model_save_path}.")

    except Exception as e:
        logging.error(f"Error during model training or saving: {e}")
        return

    logging.info("Generating recommendations...")
    recommendations = recommend_land_use_changes(df)
    for region, rec in recommendations:
        print(f"Region: {region}, Recommendation: {rec}")

if __name__ == "__main__":
    main()