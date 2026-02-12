import pygame
from client.config import assets
from client.domain.mob.mob import Mob
from utils.aseprite_reader import AsepriteReader
from utils.resource_path import resource_path
import os

class Skeleton(Mob) :

    def __init__(self, x,y,pos_chunk,cell_size,state):

        super().__init__(x,y,cell_size,size=(10,10))

        self.name = "Skeleton"
        self.chunk = pos_chunk
        self.state = state
        self.frame_perso = []
        self.frame = 0
        #self.width ,self.height = self.Img.get_size() #Get la taille de l'img
        self.frame_multiplier = 0

        self.init_Img(cell_size)

    def init_Img(self,cell_size):
        aseprite_path = resource_path("assets/sprites/monster/skeleton.aseprite")
        
        if os.path.exists(aseprite_path):
            try:
                reader = AsepriteReader(aseprite_path)
                if reader.frames:
                    for surface in reader.frames:
                        scaled_surf = pygame.transform.scale(surface, (10*cell_size, 10*cell_size))
                        self.frame_perso.append(scaled_surf)
                    return
            except Exception as e:
                print(f"Failed to load aseprite: {e}")

        # Fallback to PNGs if aseprite fails
        for i in range(4):
            
            Img = pygame.image.load(assets.MONSTER_IDLE[i]).convert_alpha() #convert_alpha() pour le fond vide
            Img = pygame.transform.scale(Img,(10*cell_size,10*cell_size))
            self.frame_perso.append(Img)

    def update_frame(self):
        self.frame_multiplier +=1
        if self.frame_multiplier >= 100 :
            self.frame +=1
            self.frame_multiplier = 0

    def blit(self,screen,x,y):
        screen.blit(self.frame_perso[self.frame%4],self.calculate_pos_blit(x,y))

        if self.state == 0: # Idle
            self.update_frame()
        else:
            self.frame = 0 # Reset to first frame (static) for other states