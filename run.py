import subprocess
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define the correct path to main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Project directory
MAIN_PATH = os.path.join(BASE_DIR, "src", "main.py")  # Full path to main.py

try:
    logging.info(f"Running {MAIN_PATH}...")
    subprocess.run(["python", MAIN_PATH], check=True)
except subprocess.CalledProcessError as e:
    logging.error(f"Failed to run main.py: {e}")
