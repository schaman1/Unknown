import pygame
import numpy as np
from serv.config import assets
from shared.constants.world import LEN_X_CHUNK,LEN_Y_CHUNK
from shared.constants.world import SCALE_BLOC

class Read_map:
    """Contient toute la physique des particules du jeu !!!! Pas plus d'explication mais il faudrait faire des sous fonctions"""
    def __init__(self):

        self.type = {"EMPTY": 0, "FIRE": 1, "STONE": 2, "GRASS": 3, "WOOD": 4, "SAND":5, "EXPLO":6, "WATER" : 7}
        self.dur = [self.type["STONE"],self.type["SAND"]] #Le min et le max
        self.vide = [self.type["EMPTY"],self.type["FIRE"]] #Le min et le max
        self.liquid = [self.type["EXPLO"],self.type["WATER"]] #Le min et le max

        self.map_chunk = []
        self.scale = SCALE_BLOC

        size = pygame.image.load(assets.BG_MAP[0][0]).convert().get_size()

        self.width_chunk,self.height_chunk = size[0]*self.scale,size[1]*self.scale
        self.len_x_chunk = LEN_X_CHUNK
        self.len_y_chunk = LEN_Y_CHUNK

        #print(self.width_chunk,self.height_chunk,"Width, Height")

        self.create_map()

    def return_type(self,y,x):

        #y = int(y)
        #x = int(x)

        chunk_y = y//self.height_chunk
        chunk_x = x//self.width_chunk

        deltay = y%self.height_chunk
        deltax = x%self.width_chunk

        if (chunk_y<0 or chunk_y >= self.len_y_chunk or chunk_x<0 or chunk_x >= self.len_x_chunk):
            return self.type["STONE"]
        #print(chunk_y)

        return self.map_chunk[chunk_y][chunk_x][deltay,deltax]

    def create_map(self):

        for y in range(self.len_y_chunk):

            col = []

            for x in range(self.len_x_chunk):

                try :

                    img = pygame.image.load(assets.BG_MAP[y][x]).convert()

                except :
                    
                    img = pygame.image.load(assets.BLACK_LAYER).convert()


                col.append(self.create_chunk(img))

            self.map_chunk.append(col)

    def create_chunk(self,img):

        grid_type = np.zeros((self.height_chunk, self.width_chunk), dtype=np.uint8)

        img_np = np.transpose(pygame.surfarray.array3d(img), (1, 0, 2))

        grid_pixels = img_np[0:self.height_chunk, 0:self.width_chunk]
        
        grid_pixels = np.repeat(grid_pixels, self.scale, axis=0)
        grid_pixels = np.repeat(grid_pixels, self.scale, axis=1)

        #mask_sand = (grid_pixels[:, :, 0] == 255) & (grid_pixels[:, :, 1] == 255) & (grid_pixels[:, :, 2] == 0)
        #mask_water = (grid_pixels[:, :, 0] == 0) & (grid_pixels[:, :, 1] == 0) & (grid_pixels[:, :, 2] == 255)
        #mask_wood = (grid_pixels[:, :, 0] == 0) & (grid_pixels[:, :, 1] == 0) & (grid_pixels[:, :, 2] == 0)
        #mask_fire = (grid_pixels[:, :, 0] == 255) & (grid_pixels[:, :, 1] == 0) & (grid_pixels[:, :, 2] == 0)
        mask_stone = (grid_pixels[:, :, 0] == 108) & (grid_pixels[:, :, 1] == 143) & (grid_pixels[:, :, 2] == 29)
        #mask_explo = (grid_pixels[:, :, 0] == 255) & (grid_pixels[:, :, 1] == 127) & (grid_pixels[:, :, 1] == 127)

        #grid_type[mask_sand] = self.type["SAND"]
        #grid_type[mask_water] = self.type["WATER"]
        #grid_type[mask_wood] = self.type["WOOD"]
        #grid_type[mask_fire] = self.type["FIRE"]
        grid_type[mask_stone] = self.type["STONE"]

        #grid_type[mask_explo] = self.type["EXPLO"]

        return grid_type