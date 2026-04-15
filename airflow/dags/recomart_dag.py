"""recomart_dag.py — Airflow DAG for RecoMart End-to-End Data Pipeline


Features: PythonOperators, failure/success callbacks, JSON monitoring logs.
"""

import logging
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from types import SimpleNamespace

# ── Configuration ─────────────────────────────────────────────────────────────
PIPELINE_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',  '..','scripts')
MONITOR_LOG  = os.path.join(PIPELINE_SRC,  '..',  'logs', 'orchestration_monitor.json')
# relative path for subprocess calls

PROJECT_ROOT = os.path.abspath(os.path.join(PIPELINE_SRC, '..'))
print(PIPELINE_SRC, MONITOR_LOG, PROJECT_ROOT)
logger = logging.getLogger(__name__)

print(PIPELINE_SRC, MONITOR_LOG)
logger = logging.getLogger(__name__)


# ── Callbacks ─────────────────────────────────────────────────────────────────
def _write_monitor(task_id: str, status: str, context: dict = None):
    """Append a JSON status entry to the orchestration monitor log."""
    os.makedirs(os.path.dirname(MONITOR_LOG), exist_ok=True)
    entries = []
    if os.path.exists(MONITOR_LOG):
        try:
            with open(MONITOR_LOG, 'r') as f:
                entries = json.load(f)
        except Exception:
            pass
    entries.append({
        "task_id":   task_id,
        "status":    status,
        "timestamp": datetime.now().isoformat(),
        "run_id":    (context or {}).get('run_id', 'manual'),
    })
    with open(MONITOR_LOG, 'w') as f:
        json.dump(entries, f, indent=2)


def on_failure_callback(context):
    task_id = context['task_instance'].task_id
    logger.error("[AIRFLOW] TASK FAILED: %s | run_id=%s", task_id, context.get('run_id', 'N/A'))
    _write_monitor(task_id, 'FAILED', context)


def on_success_callback(context):
    task_id = context['task_instance'].task_id
    logger.info("[AIRFLOW] Task succeeded: %s", task_id)
    _write_monitor(task_id, 'SUCCESS', context)


# ── Task runner ───────────────────────────────────────────────────────────────
# def _run_script(script_name: str, **kwargs):
#     """Run a pipeline script via subprocess and raise on non-zero exit."""
#     path   = os.path.join(PIPELINE_SRC, script_name)
#     logger.info("[AIRFLOW] Running: %s", path)
#     result = subprocess.run([sys.executable, path], capture_output=True, text=True, cwd=PROJECT_ROOT)
#     if result.stdout:
#         logger.info(result.stdout.strip())
#     if result.returncode != 0:
#         logger.error(result.stderr.strip())
#         raise RuntimeError(f"{script_name} exited with code {result.returncode}:\n{result.stderr}")
#     logger.info("[AIRFLOW] Completed: %s", script_name)
def _run_script(script_name: str, **kwargs):
    """Run a pipeline script via subprocess and raise on non-zero exit."""
    path = os.path.join(PIPELINE_SRC, script_name)
    logger.info("[AIRFLOW] Running: %s", path)

    # Ensure the subprocess can import project-root modules (e.g. utils.py)
    env = os.environ.copy()
    env['PYTHONPATH'] = PROJECT_ROOT + os.pathsep + env.get('PYTHONPATH', '')

    result = subprocess.run([sys.executable, path], capture_output=True, text=True, cwd=PROJECT_ROOT, env=env)
    if result.stdout:
        logger.info(result.stdout.strip())
    if result.returncode != 0:
        logger.error(result.stderr.strip())
        raise RuntimeError(f"{script_name} exited with code {result.returncode}:\n{result.stderr}")
    logger.info("[AIRFLOW] Completed: %s", script_name)

# ── DAG definition ────────────────────────────────────────────────────────────
default_args = {
    'owner':               'data_engineering_team',
    'depends_on_past':     False,
    'start_date':          datetime(2026, 3, 26),
    'email_on_failure':    False,
    'email_on_retry':      False,
    'retries':             2,
    'retry_delay':         timedelta(minutes=5),
    'on_failure_callback': on_failure_callback,
    'on_success_callback': on_success_callback,
}

dag = DAG(
    'recomart_end_to_end_pipeline',
    default_args=default_args,
    description='RecoMart: ingestion -> processing -> features -> model -> versioning',
    schedule=timedelta(days=1),
    catchup=False,
    tags=['recomart', 'ml-pipeline', 'recommendation'],
)

# ── Tasks ─────────────────────────────────────────────────────────────────────
t1_ingest = PythonOperator(
    task_id='data_ingestion',
    python_callable=lambda **kw: _run_script('data_ingestion.py', **kw),
    dag=dag,
)

t2_validate = PythonOperator(
    task_id='data_validation',
    python_callable=lambda **kw: _run_script('data_processing.py', **kw),
    dag=dag,
)

t3_prepare = PythonOperator(
    task_id='preparation_and_features',
    python_callable=lambda **kw: _run_script('feature_engineering.py', **kw),
    dag=dag,
)

t4_train = PythonOperator(
    task_id='model_training',
    python_callable=lambda **kw: _run_script('model_training.py', **kw),
    dag=dag,
)


# ── Pipeline dependency chain ─────────────────────────────────────────────────
t1_ingest >> t2_validate >> t3_prepare >> t4_train 


if __name__ == "__main__":
    # Run the pipeline scripts sequentially when executed directly.
    scripts = [
        ("data_ingestion", "data_ingestion.py"),
        ("data_validation", "data_processing.py"),
        ("preparation_and_features", "feature_engineering.py"),
        ("model_training", "model_training.py"),
    ]

    for task_id, script in scripts:
        try:
            logger.info("=== Running task: %s ===", task_id)
            _run_script(script)
            # simulate success callback context
            on_success_callback({'task_instance': SimpleNamespace(task_id=task_id), 'run_id': 'manual'})
        except Exception as e:
            # simulate failure callback context and exit non-zero
            on_failure_callback({'task_instance': SimpleNamespace(task_id=task_id), 'run_id': 'manual'})
            logger.error("Pipeline stopped due to failure in %s: %s", task_id, e)
            sys.exit(1)

    logger.info("Pipeline completed successfully.")
    on_success_callback({'task_instance': SimpleNamespace(task_id='recomart_end_to_end_pipeline'), 'run_id': 'manual'})