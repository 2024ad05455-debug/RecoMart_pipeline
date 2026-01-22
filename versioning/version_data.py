import os
import subprocess
from datetime import datetime

BASE_PATH = "E:/BITS/DM4ML/RecoMart_pipeline"

RAW_PATH = os.path.join(BASE_PATH, "data", "raw")
PROCESSED_PATH = os.path.join(BASE_PATH, "data", "processed")

def run(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def version_data():
    date_tag = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # DVC versioning
    run(f"dvc add {RAW_PATH}")
    run(f"dvc add {PROCESSED_PATH}")

    # Git commit
    run("git add .")
    run(f'git commit -m "Auto dataset version update {date_tag}"')

    print("Data versioning completed successfully")

if __name__ == "__main__":
    version_data()
