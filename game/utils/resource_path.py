import sys
import os

def resource_path(relative_path):
    """Retourne le chemin absolu correct, même dans un exe PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Normalise les séparateurs avant os.path.join
    parts = relative_path.replace("\\", "/").split("/")
    return os.path.join(base_path, *parts)