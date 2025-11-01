import pygame, numpy as np
from serv.in_game.particles import Sand,Wood, Water, Fire

class Read_map:
    def __init__(self, filename, size,canva_size):
        self.width = canva_size[0]
        self.height = canva_size[1]
        self.cell_size = size
        self.cells_w = self.width // self.cell_size
        self.cells_h = self.height // self.cell_size

        self.density = (3,1)  # 1 = pleine résolution, 2 = 1 pixel sur 2, etc.

        self.map = pygame.image.load(filename).convert()
        self.map = pygame.transform.scale(self.map, (self.width, self.height))
        #self.canva = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # grille binaire + couleurs
        #self.grid = np.zeros((self.cells_h, self.cells_w), dtype=np.uint8)
        #self.objects = {}
        self.grid = [[None for _ in range(self.cells_w)] for _ in range(self.cells_h)]
        
        # sets plutôt que listes = O(1) lookup, remove, add
        self.cell_to_update = set()
        self.circle_patterns = {}
        self.border_patterns = {}

        self.read_map()
        #self.create_map()

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
        #Pour un robinet
        #for i in range(1,10):
        #    self.grid[0][5*i] = Fire(5*i,0)
        #    self.cell_to_update.add((5*i,0))
        
        return self.move_cells()

    def get_circle_pattern(self, r_cells):
        """Retourne une liste d'offsets pour un rayon donné, pré-calculée"""
        if r_cells not in self.circle_patterns:
            pattern = []
            pattern_border = []
            for dy in range(-r_cells-1, r_cells + 2):
                for dx in range(-r_cells-1, r_cells + 2):
                    if dx*dx + dy*dy <= r_cells*r_cells:
                        pattern.append((dx, dy))
                    elif dx*dx + dy*dy <= (r_cells+1)*(r_cells+1):
                        pattern_border.append((dx, dy))
            self.circle_patterns[r_cells] = pattern
            self.border_patterns[r_cells] = pattern_border
        return self.circle_patterns[r_cells]

    def what_to_do(self,x,y,size = 10):
        cx = x // self.cell_size
        cy = y // self.cell_size
        if 0 <= cx < self.cells_w and 0 <= cy < self.cells_h:
            if self.grid[cy][cx] is not None and self.grid[cy][cx].__class__.__name__ != "Wood":  # noir indestructible
                self.destroy_rect(cx,cy, size)
            elif self.grid[cy][cx] is None:
                self.create_circle_sand(cx,cy,size*2)
        return "nothing"
    
    def create_circle_sand(self,x,y, r_cells):
        for dx,dy in self.get_circle_pattern(r_cells):
            cx = x + dx
            cy = y + dy
            if 0 <= cx < self.width  and 0 <= cy < self.height :
                if cx< self.cells_w and cy < self.cells_h:
                    if self.grid[cy][cx] is None:

                        #self.grid[cy][cx] = Water(cx,cy,self.cells_w,self.cells_h)
                        self.grid[cy][cx] = Sand(cx,cy)
                        self.cell_to_update.add((cx,cy))

    def destroy_rect(self, cx, cy, r_cells):
        """Détruit un cercle de rayon 'rayon' autour de (x, y)"""

        for dx, dy in self.get_circle_pattern(r_cells):
            nx = cx + dx
            ny = cy + dy
            if 0 <= nx < self.cells_w and 0 <= ny < self.cells_h:
                if self.grid[ny][nx] is not None and self.grid[ny][nx].__class__.__name__ != "Wood":  # noir indestructible
                    # suppression dans la grille
                    self.grid[ny][nx] = None
                    # suppression graphique
                    #self.canva.fill((255, 255, 255, 0), self.rect_grid[ny][nx])

        for dx,dy in self.border_patterns[r_cells]:
            if 0 <= cx+dx < self.cells_w and 0 <= cy+dy < self.cells_h:
                self.cell_to_update.add((cx+dx,cy+dy))
            #self.draw_rect(dx+cx,dy+cy)

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
        # suppression graphique
        #self.canva.fill((255, 255, 255, 0), self.rect_grid[y][x])

    def update_cell(self, x, y,newx,newy):
        """Fait tomber une cellule"""
        # échange dans la grille

        self.grid[newy][newx], self.grid[y][x] = self.grid[y][x], self.grid[newy][newx]

        # effacer ancienne position
        #if self.grid[y][x] is None :
        #    self.canva.fill((255, 255, 255, 0), self.rect_grid[y][x])
        #else :
        #    self.canva.fill(self.grid[y][x].color, self.rect_grid[y][x])
            #self.grid[y][x].x , self.grid[y][x].y = x,y
        # dessiner à la nouvelle position
        #self.canva.fill(self.grid[newy][newx].color, self.rect_grid[newy][newx])