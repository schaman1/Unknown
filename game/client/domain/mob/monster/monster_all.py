from shared.constants import world
from client.domain.mob.monster import monster

class Monster_all :

    def __init__(self,cell_size):

        self.dic_monster = {} #Liste des monstres dans la map
        self.init_dico_dic_monsters()
        self.cell_size = cell_size

    def init_dico_dic_monsters(self):
        for i in range(world.LEN_Y_CHUNK) :
            for j in range(world.LEN_Y_CHUNK) :
                self.dic_monster[i*100+j] = {}

    def change_chunk(self,l):
        """Change chunk for monsters"""
        for chunk,new_chunk,id in l:
            monster =  self.dic_monster[chunk][id]
            del self.dic_monster[chunk][id]
            self.dic_monster[new_chunk][id] = monster

    def init_monster(self,lchunck_monsters):
        """Initialise les monstres reçus du serv"""

        for (chunk, id, x, y, name,side) in lchunck_monsters :

            if name == 0:
                self.dic_monster[chunk][id] = monster.Skeleton(x,y,chunk,self.cell_size,0)#0 bcs state default = idle

            elif name == 1:
                self.dic_monster[chunk][id] = monster.Laseroide(x,y,chunk,self.cell_size,0)#0 bcs state default = idle

            elif name == 2:
                self.dic_monster[chunk][id] = monster.Foulli(x,y,chunk,self.cell_size,0)#0 bcs state default = idle

            elif name == 3:
                self.dic_monster[chunk][id] = monster.Defendeur(x,y,chunk,self.cell_size,0)#0 bcs state default = idle
            
            elif name == 4:
                self.dic_monster[chunk][id] = monster.Escargot(x,y,chunk,self.cell_size,0)#0 bcs state default = idle

            elif name == 5:
                self.dic_monster[chunk][id] =  monster.Limace(x, y, chunk, self.cell_size, 0) #state 0 == idle

            elif name == 6:
                self.dic_monster[chunk][id] = monster.DwarfKing(x, y, chunk, self.cell_size, 0) #Boss : Le Roi Nain

            elif name == 7:
                self.dic_monster[chunk][id] = monster.Wall(x, y, chunk, self.cell_size, 0) #Boss : Le Roi Nain

            else :
                print("Unknown monster name in client/domain/mob/monster/monster_all :",name)


    def blit_monster(self,monster,screen,x,y,dt):
        """Blit le monstre avec l'id id_monster sur le canva des monstres"""
        monster.blit(screen,x,y,dt)
    
    def blit_all_monsters(self,screen,x,y,dt):
        """Blit tout les monstres sur le canva des monstres"""

        for pos in self.dic_monster :
            for id_monster in self.dic_monster[pos] :
                self.blit_monster(self.dic_monster[pos][id_monster],screen,x,y,dt)

    def destroy_monster(self,l):

        for monster in l:

            chunk,id = monster
            del self.dic_monster[chunk][id]