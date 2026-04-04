from client.domain.mob.pnj.pnj import Pnj
from shared.constants import world
import json
import math
import pygame

class Pnj_all :

    def __init__(self,cell_size,screenSize):
        self.container_pnj = []
        self.id_compteur = 0
        self.color_compteur = 0
        self.cell_size = cell_size
        self.distance_max_blit = screenSize[1]
        self.distance_max_trigger = world.NBR_CELL_CAN_SEE*cell_size

        self.pos_blit_text = screenSize[1]-10*self.cell_size

        self.interact_img = pygame.image.load("assets/ui/infos/interact.png")
        self.interact_img = pygame.transform.scale(self.interact_img,(10*cell_size,1*cell_size))
        self.white_surf = pygame.Surface((screenSize[0],cell_size*10),pygame.SRCALPHA)

        self.is_talking = False
        self.talks_to = None


        with open("client/ui/text.json") as f:

            self.dialogues = json.load(f)
            f.close()

        self.init_pnj()

    def init_pnj(self):
        
        pos = (387,1689)
        self.add_pnj(pos,'pnj_intro')

    def add_pnj(self,pos,name):
        ele = Pnj(pos,self.color_compteur,self.id_compteur,self.cell_size,self.dialogues[name])
        self.container_pnj.append(ele)
        self.update_values()

    def update_values(self):
        self.id_compteur+=1
        self.color_compteur = (self.color_compteur+1)%4

    def blit_pnj(self,screen,x,y,dt,pos_player):
        
        for pnj in self.container_pnj :

            dist = self.distance(pos_player,pnj)

            if dist<self.distance_max_blit :

                pnj.blit(screen,x,y,dt)

                if dist<self.distance_max_trigger:
                    self.blit_interact_info(screen,pnj)

    def blit_dialogue(self,screen,dt):

        if self.is_talking :
            self.white_surf.fill((50,50,55))
            self.talks_to.blit_dialogue(self.white_surf,dt)
            screen.blit(self.white_surf,(0,self.pos_blit_text))

    def blit_interact_info(self,screen,element):
        
        pos_x = element.pos_blit[0] + element.width//2*self.cell_size  - 5*self.cell_size
        pos_y = element.pos_blit[1] - self.cell_size*1

        screen.blit(self.interact_img,(pos_x,pos_y))


    def test_trigger(self,pos_player):
        
        for pnj in self.container_pnj :

            dist = self.distance(pos_player,pnj)

            if dist<self.distance_max_trigger :

                self.is_talking = True
                self.talks_to = pnj

                return True
            
        return False

    def distance(self,pos_player,pnj):

        dist = (pos_player[0]-pnj.pos_x)**2 + (pos_player[1]-pnj.pos_y)**2
        return math.sqrt(dist)
    
    def press_enter(self):
        
        if self.talks_to!=None:

            end_text = self.talks_to.text.press_enter()
            if end_text :
                self.stop_talk()
                
                return False

            return True
        
        else :
            return False

    def stop_talk(self):
        self.is_talking = False
        self.talks_to = None