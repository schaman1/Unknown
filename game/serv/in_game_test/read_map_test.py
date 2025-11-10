import pygame, heapq
import numpy as np
from numba import njit
from numba.typed import List
from serv.in_game.particles import Sand, Wood, Water, Fire

class Read_map:
    """Contient toute la physique des particules du jeu !!!! Pas plus d'explication mais il faudrait faire des sous fonctions"""
    def __init__(self, filename):

        self.type = {"EMPTY": 0, "SAND": 1, "WATER": 2, "WOOD": 3, "FIRE": 4, "STONE":5, "GRASS":6 }#"EXPLO" : 5}
        self.propagation = {"WOOD": 98}#, "EXPLO" : 1}

        self.map = pygame.image.load(filename).convert()
        self.width, self.height = self.map.get_size()

        #print("image size :",self.map.get_size())
        #self.map = pygame.transform.scale(self.map, (self.width, self.height))

        self.grid_type = np.zeros((self.height, self.width), dtype=np.uint8)
        self.grid_color = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        self.r_or_l = np.zeros((self.height, self.width), dtype=np.bool) #If true = cell go left / else, cell go right
        self.temp = np.zeros((self.height, self.width), dtype=np.int16)

        self.create_map()

    def create_map(self):
        img_np = np.transpose(pygame.surfarray.array3d(self.map), (1, 0, 2))

        grid_pixels = img_np[0:self.height, 0:self.width]
        #print(grid_pixels[150, :, 1])
        mask_sand = (grid_pixels[:, :, 0] == 255) & (grid_pixels[:, :, 1] == 255) & (grid_pixels[:, :, 2] == 0)
        mask_water = (grid_pixels[:, :, 0] == 0) & (grid_pixels[:, :, 1] == 0) & (grid_pixels[:, :, 2] == 255)
        mask_wood = (grid_pixels[:, :, 0] == 0) & (grid_pixels[:, :, 1] == 0) & (grid_pixels[:, :, 2] == 0)
        mask_fire = (grid_pixels[:, :, 0] == 255) & (grid_pixels[:, :, 1] == 0) & (grid_pixels[:, :, 2] == 0)
        mask_stone = (grid_pixels[:, :, 0] == 127) & (grid_pixels[:, :, 1] == 127) & (grid_pixels[:, :, 2] == 127)
        #mask_explo = (grid_pixels[:, :, 0] == 255) & (grid_pixels[:, :, 1] == 127) & (grid_pixels[:, :, 1] == 127)

        # Exemple de masque spécifique
        #mask_sand[120, 3] = True

        self.grid_type[mask_sand] = self.type["SAND"]
        self.grid_type[mask_water] = self.type["WATER"]
        self.grid_type[mask_wood] = self.type["WOOD"]
        self.grid_type[mask_fire] = self.type["FIRE"]
        self.grid_type[mask_stone] = self.type["STONE"]
        #self.grid_type[mask_explo] = self.type["EXPLO"]

        self.grid_color[mask_sand] = self.random_color(mask_sand.sum(), (150, 200), (75, 140), (0, 0),255)
        self.grid_color[mask_water] = self.random_color(mask_water.sum(), (0, 20), (0, 20), (200, 255),255)
        self.grid_color[mask_wood] = self.random_color(mask_wood.sum(), (78, 88), (31, 41), (0, 0),255)
        self.grid_color[mask_fire] = self.random_color(mask_fire.sum(), (180, 255), (0, 20), (0, 0),255)
        self.grid_color[mask_stone] = self.random_color(mask_stone.sum(), (60, 75), (55, 65), (50, 60),255)
        #self.grid_color[mask_explo] = self.random_color(mask_explo.sum(), (120, 160), (120, 160), (120, 160),127)

        self.temp[mask_sand] = 60
        self.temp[mask_water] = -255
        self.temp[mask_fire] = 255
        self.temp[mask_wood] = 255
        self.temp[mask_stone] = 30
        #self.temp[mask_explo] = 255

    def random_color(self, num, r_range, g_range, b_range,transparence):
        r = np.random.randint(r_range[0], r_range[1]+1, num, dtype=np.uint8)
        g = np.random.randint(g_range[0], g_range[1]+1, num, dtype=np.uint8)
        b = np.random.randint(b_range[0], b_range[1]+1, num, dtype=np.uint8)
        a = np.full(num, transparence, dtype=np.uint8)
        return np.stack([r, g, b, a], axis=1)

    def return_all(self):
        #mask_active = self.grid_type != self.type["EMPTY"]
        #ys, xs = np.where(mask_active)
        #colors = self.grid_color[ys, xs]
        #return np.column_stack((xs, ys, colors)).tolist()
        return []

    def return_chg(self,InfoClient):
        """Retourne les chg de pixels"""

        #Robinet
        self.grid_color[0,50] = (0,0,np.random.randint(200,255),255)
        self.grid_type[0,50] = self.type["WATER"]
        self.temp[0,50] = -255

        moved_cells = move_sand_fast(
            InfoClient,
            self.grid_type,
            self.r_or_l,
            self.grid_color,
            self.temp,
            self.type["EMPTY"],
            self.type["SAND"],
            self.type["WOOD"],
            self.type["WATER"],
            self.type["FIRE"],
            self.type["STONE"],
            self.type["GRASS"],
            #self.type["EXPLO"],
            #self.propagation["EXPLO"],
            self.propagation["WOOD"]
        )
        #print(moved_cells)
        return moved_cells
    
@njit
def swap_cell(temperature,grid_type,grid_color,x,y,nx,ny):
    tmp,degre = grid_type[y, x],temperature[y,x]
    grid_type[y, x] = grid_type[ny, nx]
    temperature[y,x] = temperature[ny,nx]
    grid_type[ny, nx] = tmp
    temperature[ny,nx] = degre

    # swap couleur
    for c in range(4):
        tmpc = grid_color[y, x, c]
        grid_color[y, x, c] = grid_color[ny, nx, c]
        grid_color[ny, nx, c] = tmpc

@njit
def need_update(x:int,y:int,info):
    """Si le pixel x,y est dans le champ de vision d'un client"""

    if info[0] - info[2]//2 < x and x < info[0] + info[2]//2 :
        if info[1] - info[3]//2 < y and y < info[1] + info[3]//2 :

            return True
    return False

@njit
def create_list_update(x,y,InfoClient):
    """Itere parmis tout les clients pour savoir si le client à besoin d'avoir ce pixel à update"""
    clientToUpdate = [0]
    for idx,info in enumerate(InfoClient):
        if need_update(x,y,info):
            clientToUpdate.append(idx)
    return clientToUpdate

@njit
def set_empty(nx,ny,temperature,grid_type,grid_color,EMPTY):
    """Set nx,ny as an EMPTY cell"""
    temperature[ny,nx] = 0
    grid_type[ny,nx] = EMPTY
    grid_color[ny,nx] = (0,0,0,0)

@njit
def set_fire(nx,ny,temperature,grid_type,grid_color,FIRE):
    """Set nx,ny as an EMPTY cell"""
    temperature[ny,nx] = 255
    grid_type[ny,nx] = FIRE
    grid_color[ny,nx] = (np.random.randint(180,255),np.random.randint(0,20),0,255)

@njit
def set_grass(nx,ny,temperature,grid_type,grid_color,GRASS):
    """Set nx,ny as an EMPTY cell"""
    temperature[ny,nx] = 255
    grid_type[ny,nx] = GRASS
    grid_color[ny,nx] = (np.random.randint(60,75),np.random.randint(100,120),np.random.randint(50,60),255)

@njit
def swap_r_or_l(r_or_l,y,x,ny,nx):
    """Swap the cell for r_or_l"""
    tmp = r_or_l[y,x]
    r_or_l[y,x] = r_or_l[ny,nx]
    r_or_l[ny,nx] = tmp

@njit
def move_down_r_l(x,y,H,W,temperature,grid_type,grid_color,ISEMPTY,BECOMEEMPTY,EMPTY): #ASEMPTY = empty pour la cell specifique
    """Return nx,ny if can move down, or down-right or down-left else : None"""
    ny = y + 1
    if ny >= H : 
        return (False,0,0)

    # test bas, bas-gauche, bas-droite
    if grid_type[ny, x] in ISEMPTY:
        nx = x
    elif x > 0 and grid_type[ny, x - 1] in ISEMPTY:
        nx = x - 1
    elif x < W - 1 and grid_type[ny, x + 1] in ISEMPTY:
        nx = x + 1
    else:
        return (False,0,0)

    # swap type
    if grid_type[ny,nx] in BECOMEEMPTY:
        set_empty(nx,ny,temperature,grid_type,grid_color,EMPTY)
    return (True,nx,ny)

@njit
def move_r_or_l(x,y,W,r_or_l,temperature,grid_type,grid_color,ISEMPTY,BECOMEEMPTY,EMPTY):
    if r_or_l[y,x] is True :
        dx = -1
    else : dx = 1

    if x < W - dx and grid_type[y, x + dx] in ISEMPTY:
        nx = x + dx
        temperature[y,x] += 2

    elif x > 0 and grid_type[y, x - dx] in ISEMPTY:
        nx = x - dx
        r_or_l[y,x] = False
        temperature[y,x] += 2

    else :
        return (False,0)
        
    if grid_type[y,nx] in BECOMEEMPTY :
        set_empty(nx,y,temperature,grid_type,grid_color,EMPTY)

    return (True,nx)

@njit
def change_pos(clientToUpdate,x,y,nx,ny,moved_cells,updated,temperature,grid_type,grid_color):
    """Change the pos of the cell with it's nx,ny"""
    #else :
    swap_cell(temperature,grid_type,grid_color,x,y,nx,ny)

    # on enregistre les 2 cases modifiées
    set_move(clientToUpdate,nx,ny,updated,moved_cells,grid_color)
    set_moved_cells(clientToUpdate,x,y,moved_cells,grid_color)

@njit
def set_moved_cells(clientToUpdate,x,y,moved_cells,grid_color):
    #moved_cells[0].append([x,y,grid_color[y,x]])
    return
    for client in clientToUpdate : #List->int
        moved_cells[client].append((x, y,
                            grid_color[y, x, 0],
                            grid_color[y, x, 1],
                            grid_color[y, x, 2],
                            grid_color[y, x, 3]))

@njit
def set_move(clientToUpdate,x,y,updated,moved_cells,grid_color):
    """Set as move and to update the cell"""
    updated[y,x] = True
    set_moved_cells(clientToUpdate,x,y,moved_cells,grid_color)

@njit
def return_cell_update(lClient,H,W):
    visible = np.zeros((len(lClient),H,W),dtype=np.bool_)
    for i,(x,y,screenx,screeny) in enumerate(lClient) :
        xs = max(x-screenx//2,0)
        xe = min(x+screenx//2,W)
        ys = max(y-screeny//2,0)
        ye = min(y+screeny//2,H)

        visible[i,ys:ye,xs:xe] = True

    return visible

@njit
def move_sand_fast(InfoClient,grid_type, r_or_l,grid_color, temperature, EMPTY,SAND,WOOD,WATER,FIRE,STONE,GRASS,BurnaWood):
    l= [[(0,0,0,0,0,0),],]
    return l
    H, W = grid_type.shape

    moved_cells = []
    for i in range(len(InfoClient)):
        sublist = []
        sublist.append((0,0,0,0,0,0))
        moved_cells.append(sublist)

    updated = np.zeros((H, W), dtype=np.bool)  # masque des cellules déjà modifiées

    cell_visible = return_cell_update(InfoClient,H,W)

    # Création d'un masque combiné : une cellule est visible si au moins 1 client la voit
    visible_any = np.any(cell_visible, axis=0)  # shape = (H, W)

    # Récupérer toutes les coordonnées visibles
    yl, xl = np.nonzero(visible_any)

    #for y in range(H - 1, -1, -1):
    #    for x in range(W-1,-1,-1):
    for i in range(len(xl)):
            x = xl[i]
            y = yl[i]

            #clientToUpdate = create_list_update(x,y,InfoClient)
            #clientToUpdate.pop()
            clientToUpdate = np.nonzero(cell_visible[:,y,x])[0]
            #print(clientToUpdate)
            #print(clientToUpdate)

            if len(clientToUpdate) == 0 :
                continue

            if updated[y,x] : 
                continue

            typ = grid_type[y, x]

            if typ == SAND:
                #continue
                chg,nx,ny = move_down_r_l(x,y,H,W,temperature,grid_type,grid_color,(EMPTY,WATER,FIRE),(FIRE,),EMPTY)
                if chg is True:
                    change_pos(clientToUpdate,x,y,nx,ny,moved_cells,updated,temperature,grid_type,grid_color)
                
            elif typ == WATER :#or typ == EXPLO :
                #continue

                #if typ == WATER :
                transmax = 255
                #else :
                #    transmax = 127
                chg,nx,ny = move_down_r_l(x,y,H,W,temperature,grid_type,grid_color,(EMPTY,FIRE),(FIRE,),EMPTY)
                if chg is True :
                    temperature[y,x] = -transmax
                    #set_moved_cells(clientToUpdate,x,y,moved_cells,grid_color) #Test1

                else:
                    ny = y
                    if -50 < temperature[y,x] : #cellule meurt
                        set_empty(x,y,temperature,grid_type,grid_color,EMPTY)
                        #set_moved_cells(clientToUpdate,x,y,moved_cells,grid_color) #Test1
                        continue

                    chg,nx = move_r_or_l(x,y,W,r_or_l,temperature,grid_type,grid_color,(EMPTY,FIRE),(FIRE,),EMPTY)
                    if chg is False :
                        if temperature[y,x] > -transmax :
                            temperature[y,x] -= 1

                            if temperature[y,x] < -transmax :
                                temperature[y,x] = -transmax

                            grid_color[y,x,3] = -temperature[y,x]
                            set_moved_cells(clientToUpdate,x,y,moved_cells,grid_color)
                        continue

                grid_color[y,x,3] = -temperature[y,x]
                #else :
                change_pos(clientToUpdate,x,y,nx,ny,moved_cells,updated,temperature,grid_type,grid_color)
                swap_r_or_l(r_or_l,y,x,ny,nx)

                # on enregistre les 2 cases modifiées

            elif typ == FIRE:
                #continue
                new_temp = temperature[y,x]
                #new_life = np.zeros(4,dtype = np.int16)
                for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
                    dy = y + i
                    dx = x + j
                    if dy < 0 or dy >= H or dx < 0 or dx >= W :
                        new_temp -= 255 
                        continue

                    temp = temperature[dy,dx]
                    typ2 = grid_type[dy,dx]
                    #if temp < 0 :
                    new_temp += temp

                    if typ2 == WOOD :#or typ2 == EXPLO:
                        #if typ2 == WOOD :
                        seuil = BurnaWood 
                        #else : seuil = BurnaExplo
                        if np.random.randint(0,100) > seuil :
                            set_fire(dx,dy,temperature,grid_type,grid_color,FIRE)

                            set_move(clientToUpdate,dx,dy,updated,moved_cells,grid_color)
                        #grid[self.dx][self.x+j] = Fire(self.dx,self.y+i,255)

                new_temp = (new_temp)//5-6
                temperature[y,x] = new_temp
                grid_color[y,x,3] = new_temp

                if temperature[y,x] < 20 :
                    set_empty(x,y,temperature,grid_type,grid_color,EMPTY)
                    # on enregistre les cases modifiées
                    set_move(clientToUpdate,x,y,updated,moved_cells,grid_color)
                    continue
                

                if np.random.randint(0,101) > 50:
                    choice = np.random.randint(-1, 2)
                    if 0< x + choice and x+choice < W and 0<y -1 and grid_type[y-1,x+choice] == EMPTY:
                        dy = y-1
                        dx = x + choice
                        set_fire(dx,dy,temperature,grid_type,grid_color,FIRE)
                        # on enregistre les cases modifiées
                        set_move(clientToUpdate,dx,dy,updated,moved_cells,grid_color)
                    
                set_moved_cells(clientToUpdate,x,y,moved_cells,grid_color)
                
            elif typ == STONE :
                #continue
                r = np.random.randint(0,100000)

                ny = y + 1
                if ny >= H :
                    continue

                for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
                    dy = y +i
                    dx = x + j
                    if dy < 0 or dy >= H or dx < 0 or dx >= W :
                        #Stoppe la boucle
                        continue

                    elif grid_type[dy,dx] in (EMPTY,WATER):
                        if r > 99998 :
                            set_grass(x,y,temperature,grid_type,grid_color,GRASS)

                        set_moved_cells(clientToUpdate,x,y,moved_cells,grid_color)

            elif typ == GRASS :
                nbrGrass = 0
                for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
                    dy = y +i
                    dx = x + j
                    r = np.random.randint(0,1000)

                    if dy < 0 or dy >= H or dx < 0 or dx >= W :
                        continue

                    elif r > 997 and grid_type[dy,dx] != GRASS:
                        for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
                            ddy = dy +i
                            ddx = dx + j
                            if grid_type[ddy,ddx] == GRASS :
                                nbrGrass +=1
                        if nbrGrass < 2 or nbrGrass == 4:
                            set_grass(dx,dy,temperature,grid_type,grid_color,GRASS)
                            set_move(clientToUpdate,dx,dy,updated,moved_cells,grid_color)

    #print(moved_cells)
    return moved_cells