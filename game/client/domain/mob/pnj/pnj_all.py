from client.domain.mob.pnj.pnj import Pnj
import math

class Pnj_all :

    def __init__(self,cell_size,screenSize):
        self.container_pnj = []
        self.id_compteur = 0
        self.color_compteur = 0
        self.cell_size = cell_size
        self.distance_max_blit = screenSize[0]

        self.init_pnj()

    def init_pnj(self):
        
        pos = (387,1689)
        self.add_pnj(pos)

    def add_pnj(self,pos):
        ele = Pnj(pos,self.color_compteur,self.id_compteur,self.cell_size)
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

    def distance(self,pos_player,pnj):

        dist = (pos_player[0]-pnj.pos_x)**2 + (pos_player[1]-pnj.pos_y)**2
        return math.sqrt(dist)