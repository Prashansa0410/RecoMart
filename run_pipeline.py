# """
# RecoMart - Master Pipeline Orchestrator
# Runs entire pipeline: Ingestion → Processing → Features → Model
# """

# import sys
# from pathlib import Path
# import logging

# # Add project root to path
# sys.path.insert(0, str(Path(__file__).parent))

# from scripts.data_ingestion import run_ingestion_pipeline
# from config import LOGS_DIR
# from utils import setup_logger

# # Setup main logger
# main_logger = setup_logger('pipeline', LOGS_DIR / 'pipeline.log')


# def run_pipeline():
#     """
#     Execute complete RecoMart pipeline
#     """
#     main_logger.info("="*70)
#     main_logger.info(" RECOMART MASTER PIPELINE STARTED")
#     main_logger.info("="*70)
    
#     try:
#         # ✅ Correct indentation (inside try block)
#         step2_done = False
#         step3_done = False
#         step4_done = False

#         # STEP 1
#         main_logger.info("\n STEP 1: Data Ingestion (Shankar)")
#         main_logger.info("-" * 70)

#         try:
#             run_ingestion_pipeline()
#             main_logger.info("Ingestion completed successfully")
#         except Exception as e:
#             main_logger.error(f"Ingestion failed: {str(e)}")
#             return False
        
#         # STEP 2
#         main_logger.info("\n STEP 2: Data Processing & Validation (Prashansa)")
#         main_logger.info("-" * 70)

#         try:
#             from scripts.data_processing import run_data_processing
#             run_data_processing()
#             main_logger.info("Data processing completed successfully")
#             step2_done = True
#         except Exception as e:
#             main_logger.error(f"Data processing failed: {str(e)}")
#             return False
        
#         # STEP 3
#         main_logger.info("\n STEP 3: Feature Engineering (Aniket)")
#         main_logger.info("-" * 70)

#         try:
#             from scripts.feature_engineering import run_feature_engineering
#             run_feature_engineering()
#             main_logger.info("Feature engineering completed successfully")
#             step3_done = True
#         except Exception as e:
#             main_logger.error(f"Feature engineering failed: {str(e)}")
#             return False
        
#         # STEP 4
#         main_logger.info("\n STEP 4: Model Training & Evaluation (Flavia)")
#         main_logger.info("-" * 70)

#         try:
#             from scripts.model_training import run_model_training
#             run_model_training()
#             main_logger.info("Model training completed successfully")
#             step4_done = True
#         # except ImportError:
#         #     main_logger.warning("Model training module not yet implemented")
#         except Exception as e:
#             main_logger.error(f"Model training failed: {str(e)}")
#             return False
        
#         # FINAL STATUS
#         main_logger.info("\n" + "="*70)
#         main_logger.info(" PIPELINE EXECUTED SUCCESSFULLY")
#         main_logger.info("="*70)

#         main_logger.info("\nTeam members status:")
#         main_logger.info(f"  - Prashansa: {'done' if step2_done else 'pending'}")
#         main_logger.info(f"  - Aniket: {'done' if step3_done else 'pending'}")
#         main_logger.info(f"  - Flavia: {'done' if step4_done else 'pending'}")

#         return True
        
#     except Exception as e:
#         main_logger.error(f"PIPELINE FAILED: {str(e)}")
#         return False


# if __name__ == "__main__":
#     success = run_pipeline()
#     exit(0 if success else 1)









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
        # main_logger.info(" Waiting for model training module... (scripts/model_training.py)")
        try:
            from scripts.model_training import run_model_training
            run_model_training()
            main_logger.info("Model training completed successfully")
            step4_done = True
        except ImportError:
            main_logger.warning("Model training module not yet implemented")
        except Exception as e:
            main_logger.error(f"Model training failed: {str(e)}")
            return False
        
        main_logger.info("\n" + "="*70)
        main_logger.info(" PIPELINE FRAMEWORK READY")
        main_logger.info("="*70)
        main_logger.info("\nTeam members: Implement your modules in the scripts/ folder:")
        main_logger.info("  - Prashansa: done")
        main_logger.info("  - Aniket: scripts/feature_engineering.py")
        main_logger.info("  - Flavia: done")
        
        return True
        
    except Exception as e:
        main_logger.error(f"\n PIPELINE FAILED: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_pipeline()
    exit(0 if success else 1)