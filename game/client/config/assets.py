from utils.resource_path import resource_path
from shared.constants.world import LEN_X_CHUNK,LEN_Y_CHUNK

BG_GLOBAL = resource_path("assets/background/global/back.png")
MAP_SEEN = resource_path("assets/background/entities/cell.png")
MAP_UNSEEN = resource_path("assets/background/entities/monster.png")
BG_WAITING = resource_path("assets/background/global/back.png")

BG_MAP_COLORED =[]
BLACK_LAYER_UNCOLORED = resource_path("assets/background/map/X2Y1__IntGrid_layer-int.png")
BLACK_LAYER_COLORED = resource_path("assets/background/map/X2Y1.png")

for y in range(LEN_Y_CHUNK):

    col = []

    for x in range(LEN_X_CHUNK):

        col.append(resource_path(f"assets/background/map/X{x}Y{y}.png"))

    BG_MAP_COLORED.append(col)

BTN = resource_path("assets/ui/buttons/btn_default.png")
BTN_HOVER = resource_path("assets/ui/buttons/btn_hover.png")
ICONE_SPELL = resource_path("assets/ui/buttons/icone_spell.png")

SPELLS = []
SPELLS.append(None) #POS 0
SPELLS.append(resource_path("assets/sprites/projectile/projectile_1_0.png")) #Pos 1
SPELLS.append(resource_path("assets/sprites/projectile/projectile_0_0.png"))
SPELLS.append(resource_path("assets/sprites/projectile/projectile_3_0.png"))#Pos 3 then have to do a boucle

PLAYER_IDLE_4 = resource_path("assets/sprites/player/idle/player_idle_4.png") 
PLAYER_IDLE_1 = resource_path("assets/sprites/player/idle/player_idle_1.png") 
PLAYER_IDLE_2 = resource_path("assets/sprites/player/idle/player_idle_2.png") 
PLAYER_IDLE_3 = resource_path("assets/sprites/player/idle/player_idle_3.png") 

PLAYER_IDLE = [PLAYER_IDLE_1,PLAYER_IDLE_2,PLAYER_IDLE_3,PLAYER_IDLE_4]

MONSTER_IDLE_4 = resource_path("assets/sprites/monster/idle/monster_idle_4.png") 
MONSTER_IDLE_1 = resource_path("assets/sprites/monster/idle/monster_idle_1.png") 
MONSTER_IDLE_2 = resource_path("assets/sprites/monster/idle/monster_idle_2.png") 
MONSTER_IDLE_3 = resource_path("assets/sprites/monster/idle/monster_idle_3.png") 

MONSTER_IDLE = [MONSTER_IDLE_1,MONSTER_IDLE_2,MONSTER_IDLE_3,MONSTER_IDLE_4]

PROJECTILE_0_0 = resource_path("assets/sprites/projectile/projectile_0_0.png") 
PROJECTILE_0_1 = resource_path("assets/sprites/projectile/projectile_0_1.png") 
PROJECTILE_0_2 = resource_path("assets/sprites/projectile/projectile_0_2.png") 
PROJECTILE_0_3 = resource_path("assets/sprites/projectile/projectile_0_3.png") 

PROJECTILE_0 = [PROJECTILE_0_0,PROJECTILE_0_1,PROJECTILE_0_2,PROJECTILE_0_3]

RANGED_WEAPON_0 = resource_path("assets/sprites/weapon/idle/ranged_weapon_0_0.png")
RANGED_WEAPON_1 = resource_path("assets/sprites/weapon/idle/ranged_weapon_0_1.png")
RANGED_WEAPON_2 = resource_path("assets/sprites/weapon/idle/ranged_weapon_0_2.png")
RANGED_WEAPON_3 = resource_path("assets/sprites/weapon/idle/ranged_weapon_0_3.png")

RANGED_WEAPON = [RANGED_WEAPON_0,RANGED_WEAPON_1,RANGED_WEAPON_2,RANGED_WEAPON_3]

PROJECTILE_2_0 = resource_path("assets/sprites/projectile/projectile_2_0.png") 
PROJECTILE_2_1 = resource_path("assets/sprites/projectile/projectile_2_0.png") 
PROJECTILE_2_2 = resource_path("assets/sprites/projectile/projectile_2_0.png") 
PROJECTILE_2_3 = resource_path("assets/sprites/projectile/projectile_2_0.png") 

PROJECTILE_2 = [PROJECTILE_2_0,PROJECTILE_2_1,PROJECTILE_2_2,PROJECTILE_2_3]