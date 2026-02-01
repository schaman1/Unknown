from utils.resource_path import resource_path
from shared.constants import world

BG_MAP =[]

BLACK_LAYER = resource_path("assets/background/map/X2Y1__IntGrid_layer-int.png")



for y in range(world.LEN_Y_CHUNK):

    col = []

    for x in range(world.LEN_X_CHUNK):


        col.append(resource_path(f"assets/background/map/X{x}Y{y}__IntGrid_layer-int.png"))

    BG_MAP.append(col)