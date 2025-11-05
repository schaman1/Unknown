import pygame, heapq
import numpy as np
from numba import njit
from numba.typed import List
from serv.in_game.particles import Sand, Wood, Water, Fire

class Read_map:
    def __init__(self, filename, size, canva_size):
        self.width, self.height = canva_size
        self.cell_size = size
        self.cells_w = self.width // self.cell_size
        self.cells_h = self.height // self.cell_size

        self.type = {"EMPTY": 0, "SAND": 1, "WATER": 2, "WOOD": 3, "FIRE": 4, "EXPLO" : 5}
        self.propagation = {"WOOD": 98, "EXPLO" : 1}

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
        mask_explo = (grid_pixels[:, :, 0] == 255) & (grid_pixels[:, :, 1] == 127) & (grid_pixels[:, :, 1] == 127)

        # Exemple de masque spécifique
        #mask_sand[120, 3] = True

        self.grid_type[mask_sand] = self.type["SAND"]
        self.grid_type[mask_water] = self.type["WATER"]
        self.grid_type[mask_wood] = self.type["WOOD"]
        self.grid_type[mask_fire] = self.type["FIRE"]
        self.grid_type[mask_explo] = self.type["EXPLO"]

        self.grid_color[mask_sand] = self.random_color(mask_sand.sum(), (150, 200), (75, 140), (0, 0),255)
        self.grid_color[mask_water] = self.random_color(mask_water.sum(), (0, 20), (0, 20), (200, 255),255)
        self.grid_color[mask_wood] = self.random_color(mask_wood.sum(), (78, 88), (31, 41), (0, 0),255)
        self.grid_color[mask_fire] = self.random_color(mask_fire.sum(), (180, 255), (0, 20), (0, 0),255)
        self.grid_color[mask_explo] = self.random_color(mask_explo.sum(), (120, 160), (120, 160), (120, 160),127)
        #self.grid_color[mask_explo] = self.random_color(mask_fire.sum(), (180, 255), (0, 20), (0, 0),255)

        self.temp[mask_sand] = -50
        self.temp[mask_water] = -255
        self.temp[mask_fire] = 255
        self.temp[mask_wood] = 255
        self.temp[mask_explo] = 255

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
            self.type["EXPLO"],
            self.propagation["EXPLO"],
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
def swap_r_or_l(r_or_l,y,x,ny,nx):
    tmp = r_or_l[y,x]
    r_or_l[y,x] = r_or_l[ny,nx]
    r_or_l[ny,nx] = tmp


@njit
def move_sand_fast(grid_type, r_or_l,  grid_color, temperature, EMPTY,SAND,WOOD,WATER,FIRE,EXPLO,BurnaExplo,BurnaWood):
    H, W = grid_type.shape
    moved_cells = []
    updated = np.zeros((H, W), dtype=np.bool)  # masque des cellules déjà modifiées

    for y in range(H - 1, -1, -1):
        for x in range(W-1,-1,-1):

            if updated[y,x] : 
                continue

            typ = grid_type[y, x]

            if typ == SAND:

                ny = y + 1
                if ny >= H : 
                    continue

                # test bas, bas-gauche, bas-droite
                if grid_type[ny, x] in (EMPTY, WATER, FIRE):
                    nx = x
                elif x > 0 and grid_type[ny, x - 1] in (EMPTY, WATER, FIRE):
                    nx = x - 1
                elif x < W - 1 and grid_type[ny, x + 1] in (EMPTY, WATER, FIRE):
                    nx = x + 1
                else:
                    continue

                # swap type
                if grid_type[ny,nx] == FIRE:
                    temperature[ny,nx] = 0
                    grid_type[ny,nx] = EMPTY
                    grid_color[ny,nx] = (0,0,0,0)
                #else :
                swap_cell(temperature,grid_type,grid_color,x,y,nx,ny)

                # on enregistre les 2 cases modifiées
                updated[ny,nx] = True
                moved_cells.append((x, y,
                                    grid_color[y, x, 0],
                                    grid_color[y, x, 1],
                                    grid_color[y, x, 2],
                                    grid_color[y, x, 3]))
                moved_cells.append((nx, ny,
                                    grid_color[ny, nx, 0],
                                    grid_color[ny, nx, 1],
                                    grid_color[ny, nx, 2],
                                    grid_color[ny, nx, 3]))
                
            if typ == WATER or typ == EXPLO :

                if typ == WATER :
                    transmax = 255
                else :
                    transmax = 127

                ny = y + 1
                if ny >= H :
                    continue

                # test bas, bas-gauche, bas-droite
                if grid_type[ny, x] in (EMPTY, FIRE):
                    nx = x
                    temperature[y,x] = -transmax
                elif x > 0 and grid_type[ny, x - 1] in (EMPTY, FIRE):
                    nx = x - 1
                    temperature[y,x] = -transmax
                elif x < W - 1 and grid_type[ny, x + 1] in (EMPTY, FIRE):
                    nx = x + 1
                    temperature[y,x] = -transmax

                else:
                    ny = y

                    if -50 < temperature[y,x] :
                        temperature[y,x] = 0
                        grid_type[y,x] = EMPTY
                        grid_color[y,x] = (0,0,0,0)

                        moved_cells.append((x, y,
                                            grid_color[y, x, 0],
                                            grid_color[y, x, 1],
                                            grid_color[y, x, 2],
                                            grid_color[y, x, 3]))
                        continue

                    if r_or_l[y,x] is True :

                        if x < W - 1 and grid_type[ny, x + 1] in (EMPTY, FIRE):
                            nx = x + 1
                            temperature[y,x] += 2
                        elif x > 0 and grid_type[ny, x - 1] in (EMPTY, FIRE):
                            nx = x - 1
                            r_or_l[y,x] = False
                            temperature[y,x] += 2
                        else :
                            if temperature[y,x] > -transmax :
                                temperature[y,x] -= 1

                                if temperature[y,x] < -transmax :
                                    temperature[y,x] = -transmax

                                grid_color[y,x,3] = -temperature[y,x]

                                moved_cells.append((x, y,
                                                    grid_color[y, x, 0],
                                                    grid_color[y, x, 1],
                                                    grid_color[y, x, 2],
                                                    grid_color[y, x, 3]))
                                continue
                            else :
                                continue

                    else :
                        if x > 0 and grid_type[ny, x - 1] in (EMPTY, FIRE):
                            nx = x - 1
                            temperature[y,x] += 2
                        elif x < W - 1 and grid_type[ny, x + 1] in (EMPTY, FIRE):
                            nx = x + 1
                            temperature[y,x] += 2
                            r_or_l[y,x] = True
                        else :
                            if temperature[y,x] > -transmax :
                                temperature[y,x] -= 1

                                if temperature[y,x] < -transmax :
                                    temperature[y,x] = -transmax

                                grid_color[y,x,3] = -temperature[y,x]
                                moved_cells.append((x, y,
                                                    grid_color[y, x, 0],
                                                    grid_color[y, x, 1],
                                                    grid_color[y, x, 2],
                                                    grid_color[y, x, 3]))
                                continue
                            else :
                                continue

                grid_color[y,x,3] = -temperature[y,x]
                
                # swap type
                if grid_type[ny,nx] == FIRE:
                    if grid_type[y,x] == WATER :
                        temperature[ny,nx] = 0
                        grid_type[ny,nx] = EMPTY
                        grid_color[ny,nx] = (0,0,0,0)
                    else :
                        temperature[y,x] = 255
                        grid_type[y,x] = FIRE
                        grid_color[y,x] = (np.random.randint(180,255),np.random.randint(0,20),0,255)

                updated[ny,nx] = True
                #else :
                swap_cell(temperature,grid_type,grid_color,x,y,nx,ny)
                swap_r_or_l(r_or_l,y,x,ny,nx)

                # on enregistre les 2 cases modifiées
                moved_cells.append((x, y,
                                    grid_color[y, x, 0],
                                    grid_color[y, x, 1],
                                    grid_color[y, x, 2],
                                    grid_color[y, x, 3]))
                moved_cells.append((nx, ny,
                                    grid_color[ny, nx, 0],
                                    grid_color[ny, nx, 1],
                                    grid_color[ny, nx, 2],
                                    grid_color[ny, nx, 3]))

            if typ == FIRE:
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

                    if typ2 == WOOD or typ2 == EXPLO:
                        if typ2 == WOOD :
                            seuil = BurnaWood 
                        else : seuil = BurnaExplo
                        if np.random.randint(0,100) > seuil :
                            temperature[dy,dx] = 255
                            grid_type[dy,dx] = FIRE
                            grid_color[dy,dx] = (np.random.randint(180,255),np.random.randint(0,20),0,255)
                            updated[dy,dx] = True
                            moved_cells.append((dx, dy,
                                                grid_color[dy,dx, 0],
                                                grid_color[dy,dx, 1],
                                                grid_color[dy,dx, 2],
                                                grid_color[dy,dx, 3]))
                        #grid[self.dx][self.x+j] = Fire(self.dx,self.y+i,255)

                new_temp = (new_temp)//5-6#np.mean(new_life) - 6
                temperature[y,x] = new_temp
                grid_color[y,x,3] = new_temp

                if temperature[y,x] < 20 :
                    temperature[y,x] = 0
                    grid_type[y,x] = EMPTY
                    grid_color[y,x] = (0,0,0,0)
                    # on enregistre les cases modifiées
                    updated[y,x] = True
                    moved_cells.append((x, y,
                                        grid_color[y, x, 0],
                                        grid_color[y, x, 1],
                                        grid_color[y, x, 2],
                                        grid_color[y, x, 3]))
                    continue
                

                if np.random.randint(0,101) > 50:
                    choice = np.random.randint(-1, 2)
                    if 0< x + choice and x+choice < W and 0<y -1 and grid_type[y-1,x+choice] == EMPTY:
                        dy = y-1
                        dx = x + choice
                        temperature[dy,dx] = 255
                        grid_type[dy,dx] = FIRE
                        grid_color[dy,dx] = (np.random.randint(180,255),np.random.randint(0,20),0,255)
                        # on enregistre les cases modifiées
                        updated[y,x] = True
                        moved_cells.append((dx, dy,
                                            grid_color[dy,dx, 0],
                                            grid_color[dy,dx, 1],
                                            grid_color[dy,dx, 2],
                                            grid_color[dy,dx, 3]))
                    
                updated[y,x] = True
                moved_cells.append((x, y,
                                    grid_color[y, x, 0],
                                    grid_color[y, x, 1],
                                    grid_color[y, x, 2],
                                    grid_color[y, x, 3]))

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