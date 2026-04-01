"""
RecoMart Data Ingestion Pipeline
Person: Shankar
Responsibility: Download CSV, Sample data, Fetch API, Save to /data/raw/
"""

import pandas as pd
import requests
import os
from pathlib import Path

from utils import setup_logger

# Initialize logger
logger = setup_logger("ingestion", Path("logs/ingestion.log"))

# Configuration
CSV_PATH = "2019-Oct.csv"
SAMPLE_SIZE = 30000
RAW_DATA_DIR = Path("data/raw")
API_ENDPOINT = "https://fakestoreapi.com/products"
API_PRODUCTS_FILE = RAW_DATA_DIR / "api_products.csv"
SAMPLE_DATA_FILE = RAW_DATA_DIR / "sample_data.csv"


def load_and_sample_csv(csv_path, sample_size=30000):
    """Load CSV and sample data"""
    try:
        logger.info(f"Loading CSV from {csv_path}...")
        df = pd.read_csv(csv_path, nrows=sample_size)
        logger.info(f"CSV loaded successfully: {len(df)} rows")
        return df
    except FileNotFoundError:
        logger.error(f"CSV file not found: {csv_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading CSV: {str(e)}")
        raise


def fetch_api_products(endpoint=API_ENDPOINT):
    """Fetch product data from API"""
    try:
        logger.info(f"Fetching API data from {endpoint}...")
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        products = response.json()
        logger.info(f"API data fetched successfully: {len(products)} products")
        return products
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching API: {str(e)}")
        raise


def convert_api_to_dataframe(api_data):
    """Convert API JSON to DataFrame"""
    try:
        df = pd.DataFrame(api_data)

        api_mapping = {
            'id': 'product_id',
            'price': 'price',
            'category': 'category',
            'rating': 'rating'
        }

        df = df.rename(columns=api_mapping)

        keep_cols = [col for col in api_mapping.values() if col in df.columns]
        df = df[keep_cols]

        logger.info(f"API data converted to DataFrame: {len(df)} rows")
        return df
    except Exception as e:
        logger.error(f"Error converting API data: {str(e)}")
        raise


def save_data(df, filepath):
    """Save DataFrame to CSV"""
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filepath, index=False)
        logger.info(f"Data saved successfully to {filepath}")
    except Exception as e:
        logger.error(f"Error saving data: {str(e)}")
        raise


def run_ingestion_pipeline(csv_path=CSV_PATH, sample_size=SAMPLE_SIZE):
    """
    Run complete ingestion pipeline
    """
    logger.info("=" * 60)
    logger.info("Starting RecoMart Data Ingestion Pipeline")
    logger.info("=" * 60)

    try:
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

        # Step 1: Load CSV
        sample_df = load_and_sample_csv(csv_path, sample_size)
        save_data(sample_df, SAMPLE_DATA_FILE)

        # Step 2: API with caching
        if API_PRODUCTS_FILE.exists():
            logger.info("Using cached API data")
            api_df = pd.read_csv(API_PRODUCTS_FILE)
        else:
            logger.info("Fetching API data...")
            api_data = fetch_api_products()
            api_df = convert_api_to_dataframe(api_data)
            save_data(api_df, API_PRODUCTS_FILE)

        logger.info("=" * 60)
        logger.info("Data Ingestion Pipeline completed successfully")
        logger.info(f"Sample data: {SAMPLE_DATA_FILE}")
        logger.info(f"API products: {API_PRODUCTS_FILE}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise


if __name__ == "__main__":
    if not os.path.exists(CSV_PATH):
        logger.warning(f"{CSV_PATH} not found in project root")
        logger.info("Download dataset from Kaggle and place in root folder")
    else:
        run_ingestion_pipeline()