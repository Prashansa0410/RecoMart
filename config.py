"""
Configuration file for RecoMart project
Shared across all team members
"""

from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FEATURES_DATA_DIR = DATA_DIR / "features"
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"
MODELS_DIR = PROJECT_ROOT / "models"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# Data files
SAMPLE_DATA_FILE = RAW_DATA_DIR / "sample_data.csv"
API_PRODUCTS_FILE = RAW_DATA_DIR / "api_products.csv"
CLEANED_DATA_FILE = PROCESSED_DATA_DIR / "cleaned_data.csv"
FEATURE_DATA_FILE = FEATURES_DATA_DIR / "feature_data.csv"

# API Configuration
API_ENDPOINT = "https://fakestoreapi.com/products"
API_TIMEOUT = 10

# Data Configuration
SAMPLE_SIZE = 30000
RANDOM_STATE = 42

# Unified Schema (FROZEN - DO NOT CHANGE)
REQUIRED_COLUMNS = {
    'user_id': 'int',
    'product_id': 'int',
    'event_time': 'datetime',
    'price': 'float',
    'category': 'string',
    'rating': 'float'
}

# Log Configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# Create all directories on import
def create_directories():
    """Create all necessary directories"""
    for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, FEATURES_DATA_DIR, 
                     LOGS_DIR, REPORTS_DIR, MODELS_DIR, SCRIPTS_DIR, NOTEBOOKS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

create_directories()
