"""
RecoMart - Master Pipeline Orchestrator
Runs entire pipeline: Ingestion → Processing → Features → Model
"""

import sys
from pathlib import Path
import logging

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from scripts.data_ingestion import run_ingestion_pipeline
from config import LOGS_DIR
from utils import setup_logger

# Setup main logger
main_logger = setup_logger('pipeline', LOGS_DIR / 'pipeline.log')


def run_pipeline():
    """
    Execute complete RecoMart pipeline
    """
    main_logger.info("="*70)
    main_logger.info(" RECOMART MASTER PIPELINE STARTED")
    main_logger.info("="*70)
    
    try:
        # Step 1: Data Ingestion (Shankar)
        main_logger.info("\n STEP 1: Data Ingestion (Shankar)")
        main_logger.info("-" * 70)
        try:
            run_ingestion_pipeline()
            main_logger.info("Ingestion completed successfully")
        except Exception as e:
            main_logger.error(f" Ingestion failed: {str(e)}")
            main_logger.warning("Pipeline paused. Waiting for Shankar to resolve data ingestion.")
            return False
        
        # Step 2: Data Processing & Validation (Prashansa)
        main_logger.info("\n STEP 2: Data Processing & Validation (Prashansa)")
        main_logger.info("-" * 70)

        try:
            from scripts.data_processing import run_data_processing
            run_data_processing()
            main_logger.info(" Data processing completed successfully")
        except Exception as e:
            main_logger.error(f" Data processing failed: {str(e)}")
            return False
        
        # Step 3: Feature Engineering (Aniket)
        main_logger.info("\n  STEP 3: Feature Engineering (Aniket)")
        main_logger.info("-" * 70)
        main_logger.info(" Waiting for feature engineering module... (scripts/feature_engineering.py)")
        
        # Step 4: Model Training & Evaluation (Flavia)
        main_logger.info("\n STEP 4: Model Training & Evaluation (Flavia)")
        main_logger.info("-" * 70)
        main_logger.info(" Waiting for model training module... (scripts/model_training.py)")
        
        main_logger.info("\n" + "="*70)
        main_logger.info(" PIPELINE FRAMEWORK READY")
        main_logger.info("="*70)
        main_logger.info("\nTeam members: Implement your modules in the scripts/ folder:")
        main_logger.info("  - Prashansa: done")
        main_logger.info("  - Aniket: scripts/feature_engineering.py")
        main_logger.info("  - Flavia: scripts/model_training.py")
        
        return True
        
    except Exception as e:
        main_logger.error(f"\n PIPELINE FAILED: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_pipeline()
    exit(0 if success else 1)
