import pygame, heapq
import numpy as np
from numba import njit
#from numba.typed import List
from serv.in_game.particles import Sand, Wood, Water, Fire

class Read_map:
    """Contient toute la physique des particules du jeu !!!! Pas plus d'explication mais il faudrait faire des sous fonctions"""
    def __init__(self, filename, size, canva_size):
        self.width, self.height = canva_size
        self.cell_size = size
        self.cells_w = self.width // self.cell_size
        self.cells_h = self.height // self.cell_size

        self.type = {"EMPTY": 0, "SAND": 1, "WATER": 2, "WOOD": 3, "FIRE": 4, "STONE":5, "GRASS":6 }#"EXPLO" : 5}
        self.propagation = {"WOOD": 98}#, "EXPLO" : 1}

        self.map = pygame.image.load(filename).convert()
        self.map = pygame.transform.scale(self.map, (self.width, self.height))

        self.grid_type = np.zeros((self.cells_h, self.cells_w), dtype=np.uint8)
        self.grid_color = np.zeros((self.cells_h, self.cells_w, 4), dtype=np.uint8)
        self.r_or_l = np.zeros((self.cells_h, self.cells_w), dtype=np.bool) #If true = cell go left / else, cell go right
        self.temp = np.zeros((self.cells_h, self.cells_w), dtype=np.int16)

        self.create_map()

    def create_map(self):
        img_np = np.transpose(pygame.surfarray.array3d(self.map), (1, 0, 2))

        grid_pixels = img_np[0:self.height:self.cell_size, 0:self.width:self.cell_size]
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
        mask_active = self.grid_type != self.type["EMPTY"]
        ys, xs = np.where(mask_active)
        colors = self.grid_color[ys, xs]
        return np.column_stack((xs, ys, colors)).tolist()

    def return_sand(self):
        self.grid_color[0,50] = (0,0,np.random.randint(200,255),255)
        self.grid_type[0,50] = self.type["WATER"]
        self.temp[0,50] = -255

        moved_cells = move_sand_fast(
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
def change_pos(x,y,nx,ny,moved_cells,updated,temperature,grid_type,grid_color):
    """Change the pos of the cell with it's nx,ny"""
    #else :
    swap_cell(temperature,grid_type,grid_color,x,y,nx,ny)

    # on enregistre les 2 cases modifiées
    set_move(nx,ny,updated,moved_cells,grid_color)
    set_moved_cells(x,y,moved_cells,grid_color)

@njit
def set_moved_cells(x,y,moved_cells,grid_color):
    moved_cells.append((x, y,
                        grid_color[y, x, 0],
                        grid_color[y, x, 1],
                        grid_color[y, x, 2],
                        grid_color[y, x, 3]))

@njit
def set_move(x,y,updated,moved_cells,grid_color):
    """Set as move and to update the cell"""
    updated[y,x] = True
    set_moved_cells(x,y,moved_cells,grid_color)

@njit
def move_sand_fast(grid_type, r_or_l,grid_color, temperature, EMPTY,SAND,WOOD,WATER,FIRE,STONE,GRASS,BurnaWood):
    H, W = grid_type.shape
    moved_cells = []
    moved_cells.append((0,0,0,0,0,0))#Pour le type de list

    updated = np.zeros((H, W), dtype=np.bool)  # masque des cellules déjà modifiées

    for y in range(H - 1, -1, -1):
        for x in range(W-1,-1,-1):

            if updated[y,x] : 
                continue

            typ = grid_type[y, x]

            if typ == SAND:
                #continue
                chg,nx,ny = move_down_r_l(x,y,H,W,temperature,grid_type,grid_color,(EMPTY,WATER,FIRE),(FIRE,),EMPTY)
                if chg is True:
                    change_pos(x,y,nx,ny,moved_cells,updated,temperature,grid_type,grid_color)
                
            elif typ == WATER :#or typ == EXPLO :
                #continue

                #if typ == WATER :
                transmax = 255
                #else :
                #    transmax = 127
                chg,nx,ny = move_down_r_l(x,y,H,W,temperature,grid_type,grid_color,(EMPTY,FIRE),(FIRE,),EMPTY)
                if chg is True :
                    temperature[y,x] = -transmax
                    #set_moved_cells(x,y,moved_cells,grid_color) #Test1

                else:
                    ny = y
                    if -50 < temperature[y,x] : #cellule meurt
                        set_empty(x,y,temperature,grid_type,grid_color,EMPTY)
                        #set_moved_cells(x,y,moved_cells,grid_color) #Test1
                        continue

                    chg,nx = move_r_or_l(x,y,W,r_or_l,temperature,grid_type,grid_color,(EMPTY,FIRE),(FIRE,),EMPTY)
                    if chg is False :
                        if temperature[y,x] > -transmax :
                            temperature[y,x] -= 1

                            if temperature[y,x] < -transmax :
                                temperature[y,x] = -transmax

                            grid_color[y,x,3] = -temperature[y,x]
                            set_moved_cells(x,y,moved_cells,grid_color)
                        continue

                grid_color[y,x,3] = -temperature[y,x]
                #else :
                change_pos(x,y,nx,ny,moved_cells,updated,temperature,grid_type,grid_color)
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

                            set_move(dx,dy,updated,moved_cells,grid_color)
                        #grid[self.dx][self.x+j] = Fire(self.dx,self.y+i,255)

                new_temp = (new_temp)//5-6
                temperature[y,x] = new_temp
                grid_color[y,x,3] = new_temp

                if temperature[y,x] < 20 :
                    set_empty(x,y,temperature,grid_type,grid_color,EMPTY)
                    # on enregistre les cases modifiées
                    set_move(x,y,updated,moved_cells,grid_color)
                    continue
                

                if np.random.randint(0,101) > 50:
                    choice = np.random.randint(-1, 2)
                    if 0< x + choice and x+choice < W and 0<y -1 and grid_type[y-1,x+choice] == EMPTY:
                        dy = y-1
                        dx = x + choice
                        set_fire(dx,dy,temperature,grid_type,grid_color,FIRE)
                        # on enregistre les cases modifiées
                        set_move(dx,dy,updated,moved_cells,grid_color)
                    
                set_moved_cells(x,y,moved_cells,grid_color)
                
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

                        set_moved_cells(x,y,moved_cells,grid_color)

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
                            set_move(dx,dy,updated,moved_cells,grid_color)

    return moved_cells


    '''def return_sandi(self):

        # --- Appels move ---
        moved_cells_list = []
        remaining_cell_local = (self.grid_type == self.type["SAND"])  # initialisation

        for dx, dy in [(0, 1), (1, 1), (-1, 1)]:
            moved_cells, remaining_cell_local = self.move(remaining_cell_local, dx, dy)
            moved_cells_list.append(moved_cells)

        # --- Empile toutes les cellules en un seul tableau numpy ---
        all_moved_cells = np.vstack(moved_cells_list)

        # --- Convertis en liste une seule fois ---
        all_moved_cells_list = all_moved_cells.tolist()

        return all_moved_cells_list

    def move(self, mask_sand, dx, dy):

        # --- Création des slices corrects ---
        if dx > 0:
            dep_x = slice(None, -dx)
            arr_x = slice(dx, None)
        elif dx < 0:
            dep_x = slice(-dx, None) #if dx != -self.cells_w else slice(None)  # pour éviter slice vide
            arr_x = slice(None, dx)
        else:  # dx == 0
            dep_x = slice(None)
            arr_x = slice(None)

        dep_y = slice(None, -dy)
        arr_y = slice(dy, None)
        #H, W = self.grid_type.shape
        empty = np.zeros_like(self.grid_type, bool)

        # Détection du vide ou de l’eau en dessous

        empty[dep_y,dep_x] = (
            (self.grid_type[arr_y,arr_x] == self.type["EMPTY"]) |
            (self.grid_type[arr_y,arr_x] == self.type["WATER"])
        )
        falling = mask_sand[dep_y,dep_x] & empty[dep_y,dep_x]

        remaining_cell = mask_sand.copy()
        remaining_cell[dep_y,dep_x] = mask_sand[dep_y,dep_x]&(~falling)

        # Aucune particule à déplacer
        if not np.any(falling):
            return (np.empty((0, 6), dtype=np.uint8),remaining_cell)

        # --- Mise à jour des types ---
        self.grid_type[dep_y,dep_x][falling] = self.type["EMPTY"]
        self.grid_type[arr_y,arr_x][falling] = self.type["SAND"]

        # --- Mise à jour des couleurs ---
        tmp = self.grid_color[dep_y,dep_x][falling].copy()
        self.grid_color[dep_y,dep_x][falling] = self.grid_color[arr_y, arr_x][falling]
        self.grid_color[arr_y, arr_x][falling] = tmp

        # --- Retourner les cellules modifiées ---
        ys, xs = np.where(falling)
        offset_x = dx if dx < 0 else 0
        new_ys, new_xs = ys + dy, xs + dx
        old_colors = self.grid_color[dep_y,dep_x][falling]
        new_colors = self.grid_color[arr_y, arr_x][falling]
        #+ offset_x
        moved_cells = np.vstack((
            np.column_stack((xs - offset_x, ys, old_colors)),
            np.column_stack((new_xs - offset_x, new_ys, new_colors))
        ))
        return (
            moved_cells,
            remaining_cell
        )


class Read_map:
    def __init__(self, filename, size,canva_size):
        self.width = canva_size[0]
        self.height = canva_size[1]
        self.cell_size = size
        self.cells_w = self.width // self.cell_size
        self.cells_h = self.height // self.cell_size

        self.map = pygame.image.load(filename).convert()
        self.map = pygame.transform.scale(self.map, (self.width, self.height))

        self.grid = [[None for _ in range(self.cells_w)] for _ in range(self.cells_h)]
        
        # sets plutôt que listes = O(1) lookup, remove, add
        self.cell_to_update = set()
        self.circle_patterns = {}
        self.border_patterns = {}

        self.read_map()

    def get_color(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.map.get_at((x, y))[:3]
        return (0, 0, 0)

    def read_map(self):
        """Lit l'image et remplit la grille de cellules"""
        for cy in range(self.cells_h):
            for cx in range(self.cells_w):
                color = self.get_color(cx * self.cell_size, cy * self.cell_size)
                if color != (255, 255, 255):
                    if color == (255, 255, 0):  # sable
                        self.grid[cy][cx] = Sand(cx,cy)
                        self.cell_to_update.add((cx,cy))
                        #color = (random.randint(90,104),random.randint(49,83),0)  # noir indestructible
                    elif color == (0, 0, 255):  # eau
                        #self.grid[cy][cx] = Sand(cx,cy)
                        self.grid[cy][cx] = Water(cx,cy,self.cells_w,self.cells_h)
                        self.cell_to_update.add((cx,cy))
                        #color = (0,0,255)
                    elif color == (255,0,0):
                        self.grid[cy][cx] = Fire(cx,cy)
                        self.cell_to_update.add((cx,cy))
                    else :
                        self.grid[cy][cx] = Wood(cx,cy)  # noir indestructible

    def return_map(self):
        """Dessine la map sur l'écran"""
        
        return self.move_cells()

    def move_cells(self):
        """Met à jour les cellules qui doivent tomber"""

        to_remove = set()
        to_add = set()
        to_update = []

        for (x, y) in self.cell_to_update:
            
            if self.grid[y][x] is not None and self.grid[y][x].__class__.__name__ != "Wood":  # si la cellule existe et n'est pas noire
                
                moved, (newx, newy), new_set = self.grid[y][x].update_position(self.grid,self.cells_h,self.cells_w)

                if moved is None:
                    self.destroy_cell(x,y)
                    to_update.append((x,y,(255,255,255,0)))
                    
                    if new_set is not None :
                        to_add |= new_set

                elif moved is True: 
                        if newx is not None:
                            if self.grid[newy][newx] is None :
                                to_update.append((x,y,(255,255,255,0)))
                            else :
                                to_update.append((x,y,self.grid[newy][newx].color))
                            #else 
                            to_update.append((newx,newy,self.grid[y][x].color))
                            self.update_cell(x,y,newx,newy)

                        if new_set is not None :
                            to_add |= new_set                 
                
            to_remove.add((x, y))

        # maj des sets en une seule opération (rapide)
        self.cell_to_update -= to_remove
        self.cell_to_update |= to_add
        return to_update

    def add_to_list(self, x, y,l):
        """Ajoute une cellule à la liste des cellules à mettre à jour"""
        if 0 <= x < self.cells_w and 0 <= y < self.cells_h:
            l.add((x, y))

    def destroy_cell(self, x, y):
        """Détruit une cellule"""
        # suppression dans la grille
        self.grid[y][x] = None

    def update_cell(self, x, y,newx,newy):
        """Fait tomber une cellule"""
        # échange dans la grille

        self.grid[newy][newx], self.grid[y][x] = self.grid[y][x], self.grid[newy][newx]'''