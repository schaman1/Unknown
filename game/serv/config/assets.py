from utils.resource_path import resource_path

BG_MAP =[]

BLACK_LAYER = resource_path("assets/background/map/X2Y1__IntGrid_layer-int.png")

len_x_map = 5
len_y_map = 5

for y in range(3):

    col = []

    for x in range(3):


        col.append(resource_path(f"assets/background/map/X{x}Y{y}__IntGrid_layer-int.png"))

    BG_MAP.append(col)


BG_MONSTER = resource_path("assets/background/entities/monster.png")