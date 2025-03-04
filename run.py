import os
import sys
import subprocess

def check_python():
    """Check if Python is installed."""
    if sys.version_info.major < 3:
        print("Python 3 is required to run this program.")
        sys.exit(1)

def install_requirements():
    """Automatically install required dependencies."""
    print(" Installing requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

def run_app():
    """Run the main.py script."""
    print(" Running main.py ...")
    subprocess.run([sys.executable, "src/main.py"], check=True)

if __name__ == "__main__":
    check_python()
    install_requirements()
    run_app()
