import sys
import os

# Ensure the root project directory is in PYTHONPATH so src imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.app import AlgoVisualizerApp

def main():
    app = AlgoVisualizerApp()
    app.run()

if __name__ == "__main__":
    main()
