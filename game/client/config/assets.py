from utils.resource_path import resource_path
from shared.constants.world import LEN_X_CHUNK,LEN_Y_CHUNK

BG_GLOBAL = resource_path("assets/background/global/back.png")
BG_END = resource_path("assets/background/bg_end.png")
MAP_SEEN = resource_path("assets/background/map/map_complete.png")
MAP_UNSEEN = resource_path("assets/background/entities/monster.png")
BG_WAITING = resource_path("assets/ui/infos/niflheim.png")
TEAM_NIKA = resource_path("assets/ui/infos/team_nika.png")

MONEY = resource_path("assets/sprites/ressources/money.png")

BG_MAP_COLORED =[]
BLACK_LAYER_UNCOLORED = resource_path("assets/background/map/X0Y0__IntGrid_layer-int.png")
BLACK_LAYER_COLORED = resource_path("assets/background/map/X0Y0.png")

for y in range(LEN_Y_CHUNK):

    col = []

    for x in range(LEN_X_CHUNK):

        col.append(resource_path(f"assets/background/map/X{x}Y{y}.png"))

    BG_MAP_COLORED.append(col)

BTN = resource_path("assets/ui/buttons/btn_default.png")
BTN_HOVER = resource_path("assets/ui/buttons/btn_hover.png")
ICONE_SPELL = resource_path("assets/ui/buttons/icone_spell.png")
ICONE_AUGMENT_WEAPON = resource_path("assets/ui/buttons/icone_augment_weapon.png")

SPELLS = {}
SPELLS[0]=None #POS 0
SPELLS[1]=resource_path("assets/sprites/projectile/projectile_1_0.png") #Pos 1
SPELLS[2] = resource_path("assets/sprites/projectile/projectile_2_0.png")
SPELLS[3] = resource_path("assets/sprites/projectile/projectile_3_0.png")#Pos 3 then have to do a boucle
SPELLS[4] = resource_path("assets/sprites/projectile/projectile_4_0.png")
SPELLS[5] = resource_path("assets/sprites/projectile/projectile_5_0.png")
SPELLS[6] = resource_path("assets/sprites/projectile/projectile_6_0.png") #En attendant
SPELLS[7] = resource_path("assets/sprites/projectile/projectile_7_0.png") #zizi jvais te faire un fist fuck
SPELLS[8] = resource_path("assets/sprites/projectile/projectile_8_0.png") 
SPELLS[9] = resource_path("assets/sprites/projectile/projectile_9_0.png") 
SPELLS[10] = resource_path("assets/sprites/projectile/projectile_10_0.png")
SPELLS[11] = resource_path("assets/sprites/projectile/projectile_11_0.png")
SPELLS[12] = resource_path("assets/sprites/projectile/projectile_12_0.png")
SPELLS[13] = resource_path("assets/sprites/projectile/projectile_13_0.png")
SPELLS[14] = resource_path("assets/sprites/projectile/projectile_14_0.png")
SPELLS[15] = resource_path("assets/sprites/projectile/projectile_15_0.png")
SPELLS[16] = resource_path("assets/sprites/projectile/projectile_16_0.png")
SPELLS[20] = resource_path("assets/sprites/projectile/projectile_20_0.png")
SPELLS[21] = resource_path("assets/sprites/projectile/projectile_21_0.png")
SPELLS[22] = resource_path("assets/sprites/projectile/projectile_22_0.png")
SPELLS[30] = resource_path("assets/sprites/projectile/projectile_30_0.png")
SPELLS[31] = resource_path("assets/sprites/projectile/projectile_31_0.png")
SPELLS[32] = resource_path("assets/sprites/projectile/projectile_32_0.png")
SPELLS[33] = resource_path("assets/sprites/projectile/projectile_33_0.png")
SPELLS[34] = resource_path("assets/sprites/projectile/projectile_34_0.png")
SPELLS[40] = resource_path("assets/sprites/projectile/projectile_40_0.png")
SPELLS[41] = resource_path("assets/sprites/projectile/projectile_41_0.png")
SPELLS[42] = resource_path("assets/sprites/projectile/projectile_42_0.png")
SPELLS[43] = resource_path("assets/sprites/projectile/projectile_43_0.png")
SPELLS[44] = resource_path("assets/sprites/projectile/projectile_44_0.png")
SPELLS[45] = resource_path("assets/sprites/projectile/projectile_45_0.png")
SPELLS[46] = resource_path("assets/sprites/projectile/projectile_46_0.png")
SPELLS[47] = resource_path("assets/sprites/projectile/projectile_47_0.png")

HEALER = resource_path("assets/objects/healer.png")
HEALER_TRIGGER = resource_path("assets/objects/healer_trigger.png")
ADD_SLOT_WEAPON = resource_path("assets/objects/add_slot.png")
ADD_2_SLOT_WEAPON = resource_path("assets/objects/add_2_slot.png")
ADD_LIFE = resource_path("assets/objects/add_life.png")
REDUCE_TIME = resource_path("assets/objects/Reduce_time.png")
CHEST_SPELL_CLOSE = resource_path("assets/objects/chest_close.png")
CHEST_SPELL_OPEN = resource_path("assets/objects/chest_open.png")
CHEST_SPELL_RARE_CLOSE = resource_path("assets/objects/chest_rare_close.png")
CHEST_SPELL_RARE_OPEN = resource_path("assets/objects/chest_rare_open.png")
CHEST_SPELL_LEGENDARY_CLOSE = resource_path("assets/objects/chest_legendary_close.png")
CHEST_SPELL_LEGENDARY_OPEN = resource_path("assets/objects/chest_legendary_open.png")
CHEST_UPGRADE_CLOSE = resource_path("assets/objects/chest_upgrade_close.png")
CHEST_UPGRADE_OPEN = resource_path("assets/objects/chest_upgrade_open.png")

PLAYER_IDLE = resource_path("assets/sprites/player/idle/player_idle.png")
PLAYER_RUNNING = resource_path("assets/sprites/player/running/player_running.png")
PLAYER_DEATH = resource_path("assets/sprites/player/death/player_death.png")
PLAYER_JUMP = resource_path("assets/sprites/player/jump/player_jump.png")
PLAYER_SURPRISE = resource_path("assets/sprites/player/special/player_fuck.png")

PNJ_IDLE = resource_path("assets/sprites/pnj/pnj_idle.png")

MONSTER_2 = resource_path("assets/sprites/monster/laseroide/laseroide_running.png")
MONSTER_2_LOADING = resource_path("assets/sprites/monster/laseroide/laseroide_loading.png")

DEFENDEUR_IDLE = resource_path("assets/sprites/monster/Defendeur/Defendeur.png")
DEFENDEUR_ATTACK = resource_path("assets/sprites/monster/Defendeur/Defendeur_attack.png")
DEFENDEUR_RUNNING = resource_path("assets/sprites/monster/Defendeur/Defendeur_running.png")

ESCARGOT_IDLE = resource_path("assets/sprites/monster/Escargot/Escargot_running.png")
ESCARGOT_ATTACK = resource_path("assets/sprites/monster/Escargot/Escargot_running.png")
ESCARGOT_RUNNING = resource_path("assets/sprites/monster/Escargot/Escargot_running.png")

SHAMAN_IDLE = resource_path("assets/sprites/monster/Shaman/Shaman_running.png")
SHAMAN_ATTACK = resource_path("assets/sprites/monster/Shaman/Shaman_attacking.png")
SHAMAN_RUNNING = resource_path("assets/sprites/monster/Shaman/Shaman_running.png")

LIMACE_IDLE = resource_path("assets/sprites/monster/Limace/Limace_running.png") #limace idle à ajouter
LIMACE_ATTACK = resource_path("assets/sprites/monster/Limace/Limace_attacking.png") #add limace attack 
LIMACE_RUNNING = resource_path("assets/sprites/monster/Limace/Limace_running.png")

MMA_JUMP = resource_path("assets/sprites/monster/Mma/mma_jump.png") #add limace attack 
MMA_RUNNING = resource_path("assets/sprites/monster/Mma/mma_running.png")
MMA_ATTACKING = resource_path("assets/sprites/monster/Mma/mma_attacking.png")

WALL_IDLE = resource_path("assets/sprites/monster/Wall/Wall_idle.png")
WALLBig_IDLE = resource_path("assets/sprites/monster/Wall/WallBig_idle.png")

FOULLI = resource_path("assets/sprites/monster/Foulli/Foulli_idle.png")
FOULLI_ATTACK = resource_path("assets/sprites/monster/Foulli/Foulli_attack.png")

MONSTER_IDLE_4 = resource_path("assets/sprites/monster/idle/monster_idle_4.png") 
MONSTER_IDLE_1 = resource_path("assets/sprites/monster/idle/monster_idle_1.png") 
MONSTER_IDLE_2 = resource_path("assets/sprites/monster/idle/monster_idle_2.png") 
MONSTER_IDLE_3 = resource_path("assets/sprites/monster/idle/monster_idle_3.png") 

MONSTER_IDLE = [MONSTER_IDLE_1,MONSTER_IDLE_2,MONSTER_IDLE_3,MONSTER_IDLE_4]

MONSTER_DIE = resource_path("assets/sprites/monster/death/tombe.png") 
TOMBE_DESTROY = resource_path("assets/sprites/monster/death/tombe_destroy.png") 

MONSTER_SKELETON = resource_path("assets/sprites/monster/skeleton.aseprite")
MONSTER_DWARF_KING = resource_path("assets/sprites/monster/BossKingDwarf.aseprite")

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

PROJECTILE_8_0 = resource_path("assets/sprites/projectile/projectile_8_1.png") 
PROJECTILE_9_0 = resource_path("assets/sprites/projectile/projectile_9_0_anim.png") 

intro_images = []
for i in range(5):
    image = resource_path(f"assets/intro/Intro-{i+1}.png")
    intro_images.append(image)

COMPLETE_INFO_BG = resource_path("assets/ui/infos/fond_complete_info.png")