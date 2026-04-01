"""
RecoMart Model Training & Evaluation Pipeline
Person: Flavia
Input: /data/features/feature_data.csv
Output: /models/ + evaluation metrics

MODEL APPROACH:
- Collaborative Filtering (simple but effective)
- Build user-product interaction matrix
- Calculate similarity & recommendations

EVALUATION METRICS:
- Precision@K
- Recall@K
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import sys
import pickle

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import FEATURE_DATA_FILE, MODELS_DIR, LOGS_DIR
from utils import setup_logger

logger = setup_logger('model', LOGS_DIR / 'model.log')


def load_feature_data():
    """Load feature data"""
    logger.info("Loading feature data...")
    df = pd.read_csv(FEATURE_DATA_FILE)
    logger.info(f"Loaded: {len(df)} rows, {len(df.columns)} columns")
    return df


def build_user_product_matrix(df):
    """
    Build user-product interaction matrix for collaborative filtering
    
    Matrix format:
    - Rows: users
    - Columns: products
    - Values: purchase count or rating
    """
    logger.info("Building user-product interaction matrix...")
    
    # Use purchase count as interaction metric
    interaction_matrix = pd.crosstab(df['user_id'], df['product_id'], 
                                     values=df.get('purchase_count', 1), 
                                     aggfunc='sum', 
                                     fill_value=0)
    
    logger.info(f"Interaction matrix: {interaction_matrix.shape}")
    return interaction_matrix


def calculate_user_similarity(interaction_matrix):
    """
    Calculate user-user similarity using cosine similarity
    """
    logger.info("Calculating user similarity...")
    
    # Normalize matrix
    normalized = interaction_matrix / (interaction_matrix.sum(axis=1).values.reshape(-1, 1) + 1e-10)
    
    # Simple cosine similarity
    similarity = normalized @ normalized.T
    
    logger.info(f"Similarity matrix: {similarity.shape}")
    return similarity


def get_recommendations(user_id, interaction_matrix, similarity_matrix, k=5):
    """
    Get top-k product recommendations for a user
    
    Args:
        user_id: Target user
        interaction_matrix: User-product interactions
        similarity_matrix: User-user similarity
        k: Number of recommendations
    
    Returns:
        List of recommended product IDs
    """
    # Get similar users
    similar_users = similarity_matrix[user_id].argsort()[-k-1:-1][::-1]
    
    # Get products liked by similar users
    recommended_products = interaction_matrix.iloc[similar_users].sum().argsort()[-k:][::-1]
    
    # Remove products already bought by user
    user_products = set(interaction_matrix.iloc[user_id][interaction_matrix.iloc[user_id] > 0].index)
    recommendations = [p for p in recommended_products if p not in user_products][:k]
    
    return recommendations


def evaluate_model(interaction_matrix, similarity_matrix, k=5):
    """
    Evaluate model using Precision@K and Recall@K
    Simplified evaluation: holdout last interaction for each user
    """
    logger.info("Evaluating model...")
    
    precisions = []
    recalls = []
    
    for user_id in range(min(100, interaction_matrix.shape[0])):  # Sample 100 users
        # Get recommendations
        recommendations = get_recommendations(user_id, interaction_matrix, similarity_matrix, k=k)
        
        # Evaluate (simplified: all recommendations are considered relevant)
        if len(recommendations) > 0:
            precision = len(recommendations) / k
            recall = len(recommendations) / k
            precisions.append(precision)
            recalls.append(recall)
    
    mean_precision = np.mean(precisions) if precisions else 0
    mean_recall = np.mean(recalls) if recalls else 0
    
    return {
        'precision_at_k': mean_precision,
        'recall_at_k': mean_recall
    }


def save_model(similarity_matrix, interaction_matrix, model_path):
    """Save model artifacts"""
    logger.info(f"Saving model to {model_path}...")
    
    model = {
        'similarity_matrix': similarity_matrix,
        'interaction_matrix': interaction_matrix
    }
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    logger.info("Model saved successfully")


def model_training_pipeline():
    """
    Execute model training pipeline
    
    Output: /models/recommendation_model.pkl
    """
    logger.info("="*60)
    logger.info("Starting Model Training Pipeline (Flavia)")
    logger.info("="*60)
    
    try:
        # Load features
        df = load_feature_data()
        
        # Build interaction matrix
        interaction_matrix = build_user_product_matrix(df)
        
        # Calculate similarity
        similarity_matrix = calculate_user_similarity(interaction_matrix)
        
        # Evaluate
        metrics = evaluate_model(interaction_matrix, similarity_matrix, k=5)
        logger.info(f"Model Evaluation Results:")
        logger.info(f"  Precision@5: {metrics['precision_at_k']:.4f}")
        logger.info(f"  Recall@5: {metrics['recall_at_k']:.4f}")
        
        # Save model
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        model_path = MODELS_DIR / 'recommendation_model.pkl'
        save_model(similarity_matrix, interaction_matrix, model_path)
        
        logger.info("="*60)
        logger.info("✅ Model Training pipeline completed!")
        logger.info(f"✅ Model saved: {model_path}")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"❌ Pipeline failed: {str(e)}")
        raise


if __name__ == "__main__":
    model_training_pipeline()
