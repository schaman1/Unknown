from PIL import Image
import os
import re

folder = "../assets/background/map"

files = [f for f in os.listdir(folder) if f.endswith("IntGrid_layer-int.png")]

# Extraire X et Y depuis le nom
def get_coords(filename):
    match = re.search(r'X(\d+)Y(\d+)', filename)
    return int(match.group(1)), int(match.group(2))

# Charger avec coords
images = [(get_coords(f), Image.open(os.path.join(folder, f))) for f in files]

# Taille d'une tile (supposée identique pour tous)
tile_w, tile_h = images[0][1].size

max_x = max(coords[0] for coords, _ in images) + 1
max_y = max(coords[1] for coords, _ in images) + 1

result = Image.new("RGB", (max_x * tile_w, max_y * tile_h))

for (x, y), img in images:
    result.paste(img, (x * tile_w, y * tile_h))

result.save("map_complete.png")