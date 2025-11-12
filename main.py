"""
Main entry point for Python Game Launcher

This launches the game selection GUI where users can choose and play
different classic arcade games.
"""

import sys
from pathlib import Path

# Add src directory to path so we can import from it
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from launcher import main

if __name__ == "__main__":
    main()
