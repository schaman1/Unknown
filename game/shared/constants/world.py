#CELL_SIZE = 20

#FOR pnj tp to boss
DIST_TO_TP_BOSS = 400
POS_BOSS = [20,190]
POS_PNJ = (220,190)
POS_RESET = (40,120)
POS_TOO_LEFT = 20

SCALE_BLOC = 4 #veut dire 1 pixel = 50 pixels
RATIO = 100

#Player
SPAWN_POINT = (8*RATIO*SCALE_BLOC,20*RATIO*SCALE_BLOC)
LEN_DEATH = 10
LEN_DEATH_PLAYER = 5
START_SEE = False

NBR_CELL_CAN_SEE = 20 #Normally, 20 !
PADDING_CANVA = 2  #Combien de cellule en plus on charge autour de l'ecran du client

BG_SIZE_SERVER = (1920,1080)

LEN_X_CHUNK = 6
LEN_Y_CHUNK = 6

#Weapon :
NBRWEAPONSTOCK = 4
UPGRADE_MINUS_REFILL_TIME = 0.2
UPGRADE_MINUS_RELOAD_TIME = 0.1

TYPE_OBJECT = {
    "SPELL":0,
    "HEALER":1,
    "UpgradeWeapon":2,
    "Chest":3,
    "UpgradeLife":4,
    "UpgradeTime":5
}
