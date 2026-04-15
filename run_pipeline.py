"""
RecoMart - Master Pipeline Orchestrator
Runs entire pipeline: Ingestion → Processing → Features → Model
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from scripts.data_ingestion import run_ingestion_pipeline
from config import LOGS_DIR
from utils import setup_logger

# Setup logger
main_logger = setup_logger('pipeline', LOGS_DIR / 'pipeline.log')

MONITOR_FILE = LOGS_DIR / "orchestration_monitor.json"


# -----------------------------
# Monitor अपडेट function
# -----------------------------
def update_monitor(task, status):
    try:
        if MONITOR_FILE.exists():
            with open(MONITOR_FILE, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append({
            "task_id": task,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "run_id": "manual"
        })

        with open(MONITOR_FILE, "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        main_logger.error(f"Monitor update failed: {str(e)}")


# -----------------------------
# Main Pipeline
# -----------------------------
def run_pipeline():

    main_logger.info("="*70)
    main_logger.info("RECOMART MASTER PIPELINE STARTED")
    main_logger.info("="*70)

    try:
        # STEP 1: Data Ingestion
        main_logger.info("\nSTEP 1: Data Ingestion")
        main_logger.info("-" * 70)

        try:
            run_ingestion_pipeline()
            update_monitor("data_ingestion", "SUCCESS")
            main_logger.info("Ingestion completed successfully")
        except Exception as e:
            update_monitor("data_ingestion", "FAILED")
            main_logger.error(f"Ingestion failed: {str(e)}")
            return False

        # STEP 2: Data Processing
        main_logger.info("\nSTEP 2: Data Processing & Validation")
        main_logger.info("-" * 70)

        try:
            from scripts.data_processing import run_data_processing
            run_data_processing()
            update_monitor("data_processing", "SUCCESS")
            main_logger.info("Data processing completed successfully")
        except Exception as e:
            update_monitor("data_processing", "FAILED")
            main_logger.error(f"Processing failed: {str(e)}")
            return False

        # STEP 3: Feature Engineering
        main_logger.info("\nSTEP 3: Feature Engineering")
        main_logger.info("-" * 70)

        try:
            from scripts.feature_engineering import run_feature_engineering
            run_feature_engineering()
            update_monitor("feature_engineering", "SUCCESS")
            main_logger.info("Feature engineering completed successfully")
        except Exception as e:
            update_monitor("feature_engineering", "FAILED")
            main_logger.error(f"Feature engineering failed: {str(e)}")
            return False

        # STEP 4: Model Training
        main_logger.info("\nSTEP 4: Model Training & Evaluation")
        main_logger.info("-" * 70)

        try:
            from scripts.model_training import run_model_training
            run_model_training()
            update_monitor("model_training", "SUCCESS")
            main_logger.info("Model training completed successfully")
        except Exception as e:
            update_monitor("model_training", "FAILED")
            main_logger.error(f"Model training failed: {str(e)}")
            return False

        # FINAL
        main_logger.info("\n" + "="*70)
        main_logger.info("PIPELINE EXECUTED SUCCESSFULLY")
        main_logger.info("="*70)

        return True

    except Exception as e:
        main_logger.error(f"PIPELINE FAILED: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_pipeline()
    exit(0 if success else 1)