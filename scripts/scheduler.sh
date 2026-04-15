import schedule
import time
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

def run_pipeline():
    print("\n Running Scheduled Pipeline...\n")
    
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "run_pipeline.py")],
        cwd=PROJECT_ROOT
    )

    if result.returncode == 0:
        print(" Pipeline executed successfully\n")
    else:
        print(" Pipeline failed\n")


# Schedule (every 1 minute for testing)
# schedule.every(1).minutes.do(run_pipeline)

# You can change later:
schedule.every().day.at("09:00").do(run_pipeline)

print(" Scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(1)