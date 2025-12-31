#Toutes les variables importantes du jeu sont ici

FPS_SERVER = 60#Ce qui va tourner sur le serv
FPS_CELL_UPDATE = 45 #Combien de fois par secondes on update les cells
FPS_CLIENT = 600 #Ce qui va tourner sur  le client #!!! je crois pas utilisé ou pas besoin

BG_CELL = "assets/bgCell.png"
BG_MONSTER = "assets/bgMonster.png"
BG_GLOBAL = "assets/bgGlobal.png"
BTN = "assets/btn.png"
BTN_HOVER = "assets/btn_hover.png"

CELL_SIZE = 12
RATIO = 100
SPAWN_POINT = (500*RATIO,140*RATIO)

PLAYER_SIZE_HEIGHT = 10
PLAYER_SIZE_WIDTH = 10

SIZE_CHUNK_MONSTER = 100  #Taille d'un chunk de monstre en pixel
BG_SIZE_SERVER = (1920,1080)#(590,430)#
NBR_CELL_CAN_SEE = 30 #Nbr de cellule que peut voir
PADDING_CANVA = 2  #Combien de cellule en plus on charge autour de l'ecran du client

PORT = 5000