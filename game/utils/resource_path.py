import sys
import os

def resource_path(relative_path):
    """Retourne le chemin absolu correct, même dans un exe PyInstaller."""
    try:
        # PyInstaller crée un dossier temporaire _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Si on est en dev, on prend le dossier parent de 'utils' donc 'game'
        # utils/resource_path.py -> utils -> game
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
