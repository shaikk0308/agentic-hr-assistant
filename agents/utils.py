from pathlib import Path

def get_project_root():
    """Return the absolute path to the project root (employee-assistant/)."""
    # This file is in agents/utils.py, so go up one level to reach project root
    return Path(__file__).resolve().parent.parent
