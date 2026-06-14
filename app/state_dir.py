# state_dir.py
import os
from pathlib import Path

def get_state_file(*paths):
    """
    Возвращает путь из STATE_DIRECTORY (который передаёт systemd)
    """
    base = Path(os.environ['STATE_DIRECTORY'])  # Берём строго из переменной
    
    if paths:
        return base.joinpath(*paths)
    return base