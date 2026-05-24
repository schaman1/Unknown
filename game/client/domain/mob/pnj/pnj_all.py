from client.domain.mob.pnj.pnj import Pnj
from shared.constants import world
from client.config import display_text
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

        self.text_entrer = display_text.FONT.render("Appuyer sur entrer",True, (255,255,255))  # True = anti-aliasing
        size = display_text.FONT.size("Appuyer sur entrer")
        self.pos_text_entrer = (screenSize[0] - size[0],screenSize[1]-size[1])

        self.pos_blit_text = screenSize[1]-10*self.cell_size

        self.interact_img = display_text.FONT_SMALL.render("E : interragir",True, (180,180,180))  # True = anti-aliasing
        self.white_surf = pygame.Surface((screenSize[0],cell_size*10),pygame.SRCALPHA)

        self.is_talking = False
        self.talks_to = None

        with open("client/ui/json/text.json") as f:

            self.dialogues = json.load(f)
            f.close()

        self.init_pnj()

    def init_pnj(self):
        
        pos = (70,125)
        self.add_pnj(pos,'pnj_tell_story')
        
        pos = (20,185)
        self.add_pnj(pos,'pnj_learn_attack')
    
        pos = (77,157)
        self.add_pnj(pos,'pnj_tell_healer')
    
        pos = (425,261)
        self.add_pnj(pos,'pnj_double_jump')
        
        pos = world.POS_PNJ
        self.add_pnj(pos,'pnj_tp_boss')

    def add_pnj(self,pos,name):

        pos = [pos[0]*self.cell_size,pos[1]*self.cell_size]

        ele = Pnj(pos,self.color_compteur,self.id_compteur,self.cell_size,self.dialogues[name],name)
        self.container_pnj.append(ele)
        self.update_values()

    def update_values(self):
        self.id_compteur+=1
        self.color_compteur = (self.color_compteur+1)%4

    def blit_pnj(self,screen,x,y,dt,pos_player):
        
        for pnj in self.container_pnj :

            dist = self.distance(pos_player,pnj)

            if dist<self.distance_max_blit :

                if pnj.pos_x < pos_player[0]:
                    pnj.animation.direction = "right"
                else :
                    pnj.animation.direction = "left"

                pnj.blit(screen,x,y,dt)

                if dist<self.distance_max_trigger:
                    self.blit_interact_info(screen,pnj)

    def blit_dialogue(self,screen,dt):

        if self.is_talking :
            self.white_surf.fill((50,50,55))
            self.talks_to.blit_dialogue(self.white_surf,dt)
            screen.blit(self.white_surf,(0,self.pos_blit_text))
            screen.blit(self.text_entrer,self.pos_text_entrer)

    def blit_interact_info(self,screen,element):
        
        pos_x = element.pos_blit[0] + element.width//2*self.cell_size  - 5*self.cell_size
        pos_y = element.pos_blit[1] - self.cell_size*1

        screen.blit(self.interact_img,(pos_x,pos_y))

    def test_trigger(self,pos_player,min_dist_other_ele):

        dist_min_pnj = [self.distance_max_blit,None]
        if min_dist_other_ele == None:
            min_dist_other_ele = self.distance_max_blit
        
        for pnj in self.container_pnj :

            dist = self.distance(pos_player,pnj)

            if dist<dist_min_pnj[0] :

                dist_min_pnj = [dist,pnj]

        if min_dist_other_ele>dist_min_pnj[0] :
            self.is_talking = True
            self.talks_to = dist_min_pnj[1]

            return True

        else :
            
            return False

    def distance(self,pos_player,pnj):

        dist = (pos_player[0]-pnj.pos_x)**2 + (pos_player[1]-pnj.pos_y)**2
        return math.sqrt(dist)
    
    def press_enter(self):
        
        if self.talks_to!=None:

            end_text = self.talks_to.text.press_enter()
            if end_text :
                pnj = self.talks_to
                self.stop_talk()
                
                return False,pnj

            return True,self.talks_to
        
        else :
            return None,None

    def stop_talk(self):
        self.is_talking = False
        self.talks_to = None

    def change_text_pnj(self,pnj_name,new_name):
        for pnj in self.container_pnj :

            if pnj.name == pnj_name:
                pnj.name = new_name
                pnj.text.text_to_blit = self.dialogues[new_name]
                pnj.text.set_lenght_text()
                pnj.text.lenght_all_texts = len(pnj.text.text_to_blit)