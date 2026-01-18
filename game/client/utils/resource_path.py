import sys
import os

def resource_path(relative_path):
    """Retourne le chemin absolu correct, même dans un exe PyInstaller."""
    try:
        # PyInstaller crée un dossier temporaire _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
