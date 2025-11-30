import pygame
import numpy as np
import serv.in_game.njitOpti.njitBoucle as njitBoucle

class Read_map:
    """Contient toute la physique des particules du jeu !!!! Pas plus d'explication mais il faudrait faire des sous fonctions"""
    def __init__(self, filename):

        self.type = {"EMPTY": 0, "FIRE": 1, "STONE": 2, "GRASS": 3, "WOOD": 4, "SAND":5, "EXPLO":6, "WATER" : 7}
        self.dur = [self.type["STONE"],self.type["SAND"]] #Le min et le max
        self.vide = [self.type["EMPTY"],self.type["FIRE"]] #Le min et le max
        self.liquid = [self.type["EXPLO"],self.type["WATER"]] #Le min et le max

        self.map = pygame.image.load(filename).convert()
        self.width, self.height = self.map.get_size()

        self.grid_type = np.zeros((self.height, self.width), dtype=np.uint8)
        self.grid_color = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        self.r_or_l = np.zeros((self.height, self.width), dtype=np.bool) #If true = cell go left / else, cell go right
        self.temp = np.zeros((self.height, self.width), dtype=np.int16)
        self.ToUpdate = np.ones((self.height,self.width),dtype = np.bool)

        self.visible = None
        self.xs = np.empty(1, dtype=np.int32)
        self.ys = np.empty(1, dtype=np.int32)

        self.create_map()

    def create_map(self):
        img_np = np.transpose(pygame.surfarray.array3d(self.map), (1, 0, 2))

        grid_pixels = img_np[0:self.height, 0:self.width]
        #print(grid_pixels[450, 530, :])
        mask_sand = (grid_pixels[:, :, 0] == 255) & (grid_pixels[:, :, 1] == 255) & (grid_pixels[:, :, 2] == 0)
        mask_water = (grid_pixels[:, :, 0] == 0) & (grid_pixels[:, :, 1] == 0) & (grid_pixels[:, :, 2] == 255)
        mask_wood = (grid_pixels[:, :, 0] == 127) & (grid_pixels[:, :, 1] == 127) & (grid_pixels[:, :, 2] == 0)
        mask_fire = (grid_pixels[:, :, 0] == 255) & (grid_pixels[:, :, 1] == 0) & (grid_pixels[:, :, 2] == 0)
        mask_stone = (grid_pixels[:, :, 0] == 127) & (grid_pixels[:, :, 1] == 127) & (grid_pixels[:, :, 2] == 127)
        mask_explo = (grid_pixels[:, :, 0] == 255) & (grid_pixels[:, :, 1] == 127) & (grid_pixels[:, :, 1] == 127)

        # Exemple de masque spécifique
        #mask_sand[120, 3] = True

        self.grid_type[mask_sand] = self.type["SAND"]
        self.grid_type[mask_water] = self.type["WATER"]
        self.grid_type[mask_wood] = self.type["WOOD"]
        self.grid_type[mask_fire] = self.type["FIRE"]
        self.grid_type[mask_stone] = self.type["STONE"]
        self.grid_type[mask_explo] = self.type["EXPLO"]

        self.grid_color[mask_sand] = self.random_color(mask_sand.sum(), (150, 200), (75, 140), (0, 0),255)
        self.grid_color[mask_water] = self.random_color(mask_water.sum(), (0, 20), (0, 20), (200, 255),255)
        self.grid_color[mask_wood] = self.random_color(mask_wood.sum(), (78, 88), (31, 41), (0, 0),255)
        self.grid_color[mask_fire] = self.random_color(mask_fire.sum(), (180, 255), (0, 20), (0, 0),255)
        self.grid_color[mask_stone] = self.random_color(mask_stone.sum(), (60, 75), (55, 65), (50, 60),255)
        self.grid_color[mask_explo] = self.random_color(mask_explo.sum(), (120, 160), (120, 160), (120, 160),127)

        self.temp[mask_sand] = 60
        self.temp[mask_water] = -255
        self.temp[mask_fire] = 255
        self.temp[mask_wood] = 255
        self.temp[mask_stone] = 30
        self.temp[mask_explo] = 255

    def random_color(self, num, r_range, g_range, b_range,transparence):
        r = np.random.randint(r_range[0], r_range[1]+1, num, dtype=np.uint8)
        g = np.random.randint(g_range[0], g_range[1]+1, num, dtype=np.uint8)
        b = np.random.randint(b_range[0], b_range[1]+1, num, dtype=np.uint8)
        a = np.full(num, transparence, dtype=np.uint8)
        return np.stack([r, g, b, a], axis=1)

    def return_all(self,lClient):
        cells = []
        for i,client in enumerate(lClient.values()):
            cells.append([])
            for column in range (client.screen_size[0]):
                deltax = column-(client.screen_size[0]//2)
                deltay = -(client.screen_size[1]//2)
                cells[i]+=(njitBoucle.return_column(client.pos_x+deltax,client.pos_y+deltay,client.screen_size[1],self.grid_color))
        
        #print(cells)
        
        return cells

    def return_chg(self,lClient):
        """Retourne les chg de pixels"""

        #Robinet
        self.grid_color[450,450] = (np.random.randint(200,255),0,0,255)
        self.grid_type[450,450] = self.type["FIRE"]
        self.temp[450,450] = 255

        self.visible = njitBoucle.return_cell_update(self.ToUpdate,lClient.values(),self.height,self.width)

        self.ys , self.xs = njitBoucle.return_x_y(self.visible)

        moved_cells = njitBoucle.move_fast(
            self.ToUpdate,
            self.visible,
            self.xs,self.ys,
            self.grid_type,
            self.r_or_l,
            self.grid_color,
            self.temp,
        ) 

        return moved_cells