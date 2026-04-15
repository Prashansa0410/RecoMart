"""
RecoMart Feature Engineering Pipeline
Person: Aniket

Input: data/processed/cleaned_data.csv
Output: data/features/feature_data.csv
"""

import pandas as pd
from pathlib import Path
import sys
import os
import ast

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import CLEANED_DATA_FILE, FEATURE_DATA_FILE


def run_feature_engineering():
    print("\n===== FEATURE ENGINEERING STARTED =====")

    try:
        # -------------------------------
        # Load data
        # -------------------------------
        print("Loading cleaned data...")
        df = pd.read_csv(CLEANED_DATA_FILE)

        print("Rows loaded:", len(df))

        # -------------------------------
        # Fix datetime
        # -------------------------------
        if 'event_time' in df.columns:
            df['event_time'] = pd.to_datetime(df['event_time'], errors='coerce')

        # -------------------------------
        # 🔥 FIX: Convert rating to numeric
        # -------------------------------
        if 'rating' in df.columns:
            print("Fixing rating column...")

            # Convert string → dict
            df['rating'] = df['rating'].apply(
                lambda x: ast.literal_eval(x) if isinstance(x, str) else x
            )

            # Extract 'rate'
            df['rating'] = df['rating'].apply(
                lambda x: x.get('rate') if isinstance(x, dict) else x
            )

            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

            print("Rating converted to numeric")

        # -------------------------------
        # Feature 1: purchase_count
        # -------------------------------
        print("Creating purchase_count...")
        purchase_count = df.groupby('user_id').size().reset_index(name='purchase_count')

        # -------------------------------
        # Feature 2: user_activity
        # -------------------------------
        print("Creating user_activity...")
        user_activity = df.groupby('user_id').agg(
            activity_events=('product_id', 'count'),
            first_event=('event_time', 'min'),
            last_event=('event_time', 'max')
        ).reset_index()

        # -------------------------------
        # Feature 3: product_popularity
        # -------------------------------
        print("Creating product_popularity...")

        agg_dict = {
            'user_id': 'count',
            'price': 'mean'
        }

        if 'rating' in df.columns:
            agg_dict['rating'] = 'mean'

        product_popularity = df.groupby('product_id').agg(agg_dict).reset_index()

        product_popularity.rename(columns={
            'user_id': 'popularity_count',
            'price': 'avg_price',
            'rating': 'avg_rating'
        }, inplace=True)

        # -------------------------------
        # Combine features
        # -------------------------------
        print("Combining features...")

        user_features = pd.merge(purchase_count, user_activity, on='user_id', how='left')

        feature_df = pd.merge(df, user_features, on='user_id', how='left')
        feature_df = pd.merge(feature_df, product_popularity, on='product_id', how='left')

        print("Final shape:", feature_df.shape)

        # -------------------------------
        # Save file
        # -------------------------------
        output_path = Path(FEATURE_DATA_FILE)

        print("Saving file to:", output_path)
        print("Absolute path:", os.path.abspath(output_path))

        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save CSV
        feature_df.to_csv(output_path, index=False)

        print("✅ feature_data.csv created successfully!")
        print("===== FEATURE ENGINEERING COMPLETED =====\n")

    except Exception as e:
        print("❌ ERROR:", str(e))
        raise


# Allow standalone run
if __name__ == "__main__":
    run_feature_engineering()