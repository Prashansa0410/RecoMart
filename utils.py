"""
Utility functions for RecoMart project
Shared across team members
"""

import pandas as pd
import logging
from config import LOG_FORMAT, LOG_LEVEL
from pathlib import Path


def setup_logger(name, log_file):
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # duplicate handlers
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(LOG_FORMAT)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def validate_schema(df, required_columns):
    """
    Validate DataFrame schema
    
    Args:
        df (pd.DataFrame): Data to validate
        required_columns (dict): Expected columns and types
    
    Returns:
        dict: Validation results
    """
    results = {
        'valid': True,
        'missing_columns': [],
        'extra_columns': [],
        'errors': []
    }
    
    # Check for missing columns
    missing = set(required_columns.keys()) - set(df.columns)
    if missing:
        results['valid'] = False
        results['missing_columns'] = list(missing)
    
    # Check for extra columns
    extra = set(df.columns) - set(required_columns.keys())
    if extra:
        results['extra_columns'] = list(extra)
    
    return results


def check_data_quality(df):
    """
    Check basic data quality
    
    Args:
        df (pd.DataFrame): Data to check
    
    Returns:
        dict: Quality metrics
    """
    quality = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'duplicates': df.duplicated().sum(),
        'missing_values': df.isnull().sum().to_dict(),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
    }
    return quality


def save_dataframe(df, filepath):
    """
    Save DataFrame to CSV with validation
    
    Args:
        df (pd.DataFrame): Data to save
        filepath (Path): Output path
    
    Returns:
        bool: Success status
    """
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filepath, index=False)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {str(e)}")
        return False


def load_dataframe(filepath):
    """
    Load DataFrame from CSV
    
    Args:
        filepath (Path): Input path
    
    Returns:
        pd.DataFrame: Loaded data
    """
    return pd.read_csv(filepath)
