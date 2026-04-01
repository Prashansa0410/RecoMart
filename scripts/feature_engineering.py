"""
RecoMart Feature Engineering Pipeline
Person: Aniket
Input: /data/processed/cleaned_data.csv
Output: /data/features/feature_data.csv

FEATURES TO CREATE:
1. purchase_count: Number of purchases per user
2. user_activity: User interaction frequency
3. product_popularity: How many times a product was purchased

Feature Definition:
- purchase_count: Aggregated by user_id
- user_activity: Events per user in time window
- product_popularity: Events per product in time window
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import CLEANED_DATA_FILE, FEATURE_DATA_FILE, LOGS_DIR
from utils import setup_logger, save_dataframe

logger = setup_logger('features', LOGS_DIR / 'features.log')


def load_cleaned_data():
    """Load cleaned data"""
    logger.info("Loading cleaned data...")
    df = pd.read_csv(CLEANED_DATA_FILE)
    logger.info(f"Loaded: {len(df)} rows")
    return df


def create_purchase_count(df):
    """
    Feature: purchase_count
    Count of purchases per user
    """
    logger.info("Creating purchase_count feature...")
    
    purchase_count = df.groupby('user_id').size().reset_index(name='purchase_count')
    
    logger.info(f"Created purchase_count for {len(purchase_count)} users")
    return purchase_count


def create_user_activity(df):
    """
    Feature: user_activity
    User interaction frequency (events per user)
    """
    logger.info("Creating user_activity feature...")
    
    user_activity = df.groupby('user_id').agg({
        'product_id': 'count',
        'event_time': ['min', 'max']
    }).reset_index()
    
    user_activity.columns = ['user_id', 'activity_events', 'first_event', 'last_event']
    
    logger.info(f"Created user_activity for {len(user_activity)} users")
    return user_activity


def create_product_popularity(df):
    """
    Feature: product_popularity
    How many times each product was purchased
    """
    logger.info("Creating product_popularity feature...")
    
    product_popularity = df.groupby('product_id').agg({
        'user_id': 'count',
        'price': 'mean',
        'rating': 'mean'
    }).reset_index()
    
    product_popularity.columns = ['product_id', 'popularity_count', 'avg_price', 'avg_rating']
    
    logger.info(f"Created product_popularity for {len(product_popularity)} products")
    return product_popularity


def combine_features(df, purchase_count, user_activity, product_popularity):
    """
    Combine all features into single feature DataFrame
    
    Strategy:
    - Merge purchase_count with user_activity on user_id
    - Merge product_popularity with main df on product_id
    """
    logger.info("Combining features...")
    
    # User features
    user_features = pd.merge(purchase_count, user_activity, on='user_id', how='left')
    
    # Add user features to main df
    feature_df = pd.merge(df, user_features, on='user_id', how='left')
    
    # Add product features
    feature_df = pd.merge(feature_df, product_popularity, on='product_id', how='left')
    
    logger.info(f"Combined feature DataFrame: {len(feature_df)} rows, {len(feature_df.columns)} columns")
    
    return feature_df


def feature_engineering_pipeline():
    """
    Execute feature engineering pipeline
    
    Output: /data/features/feature_data.csv
    """
    logger.info("="*60)
    logger.info("Starting Feature Engineering Pipeline (Aniket)")
    logger.info("="*60)
    
    try:
        # Load cleaned data
        df = load_cleaned_data()
        
        # Create features
        purchase_count = create_purchase_count(df)
        user_activity = create_user_activity(df)
        product_popularity = create_product_popularity(df)
        
        # Combine features
        feature_df = combine_features(df, purchase_count, user_activity, product_popularity)
        
        # Save features
        save_dataframe(feature_df, FEATURE_DATA_FILE)
        
        logger.info("="*60)
        logger.info("✅ Feature Engineering pipeline completed!")
        logger.info(f"✅ Output: {FEATURE_DATA_FILE}")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"❌ Pipeline failed: {str(e)}")
        raise


if __name__ == "__main__":
    feature_engineering_pipeline()
