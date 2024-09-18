import numpy as np
import pandas as pd
from PIL import Image
import logging
import os

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

def preprocess_data(image_path='data/ghg_map.png', save_path='data/preprocessed_data.npy'):
    try:
        logging.info("Starting data preprocessing...")

        # Check if image file exists
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"The image file {image_path} does not exist.")
        
        # Load the image
        try:
            image = Image.open(image_path)
            logging.info(f"Image {image_path} loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading image {image_path}: {e}")
            return None
        
        # Example image processing step: convert to grayscale
        image = image.convert('L')  # Convert image to grayscale
        image_data = np.array(image)
        logging.debug(f"Image data shape: {image_data.shape}")

        # Example DataFrame creation
        data = {
            'region': ['Region A', 'Region B', 'Region C', 'Region D'],
            'current_emissions': [150, 300, 100, 200],
            'land_use': ['forest', 'urban', 'agriculture', 'forest'],
            'population_density': [50, 200, 100, 150],
            'temperature': [15, 20, 25, 18],
            'sequestration_potential': [120, 10, 80, 110]
        }
        
        df = pd.DataFrame(data)
        logging.debug("Dataframe created successfully.")
        
        # Create target variable (future emissions prediction)
        df['future_emissions'] = df['current_emissions'] * 0.95
        
        # Convert land use to numeric values
        df['land_use_numeric'] = df['land_use'].map({'forest': 3, 'agriculture': 2, 'urban': 1})
        
        # Extract features and labels
        X = df[['current_emissions', 'population_density', 'temperature', 'sequestration_potential', 'land_use_numeric']]
        y = df['future_emissions']

        # Save features and labels to numpy file
        np.save(save_path, {'X_train': X.values, 'y_train': y.values})
        logging.info(f"Preprocessed data saved to {save_path}.")
        
        return df
    except Exception as e:
        logging.error(f"Error in data preprocessing: {e}")
        return None

# Test the preprocessing function
if __name__ == "__main__":
    df = preprocess_data()
    if df is not None:
        logging.debug(f"Preprocessed data: \n{df.head()}")
    else:
        logging.error("Failed to preprocess data.")