import pygame
from serv.in_game.C_monster import Skeleton

class Read_monster :

    def __init__(self,filename_map_monster,size_chunk) :

        self.dic_monster = {}
        self.map_monster = pygame.image.load(filename_map_monster).convert()
        self.width, self.height = self.map_monster.get_size()
        self.size_chunk = size_chunk

        self.init_dic_monster()

    def init_dic_monster(self) :

        for i in range(self.width//self.size_chunk+1) :
            for j in range(self.height//self.size_chunk+1) :
                self.dic_monster[(i,j)] = []

        self.create_list_monster()

    def return_all_monster(self,lInfoClient) :
        print(self.dic_monster)
        list_modif = []
        for i in range(len(lInfoClient)):
            list_modif.append([])
            for key in self.dic_monster :
                for monster in self.dic_monster[key] :
                    list_modif[i].append((monster.name, monster.pos_x, monster.pos_y))

        return list_modif

    def create_list_monster(self) :
        for x in range(self.width):
                for y in range(self.height):
                    color = self.map_monster.get_at((x, y))[:3]  # (r,g,b)

                    #print(f"Création d'un Skeleton en ({x}, {y})")
                    if color == (0, 0, 0):      # pixel noir = skeleton

                        self.dic_monster[(x//self.size_chunk,y//self.size_chunk)].append(Skeleton(x,y))

    def return_chg(self, lInfoClient) :
        list_modif = []
        for i,info in enumerate(lInfoClient) :
            xpos = info[0]
            ypos = info[1]
            xscreen = info[2]
            yscreen = info[3]

            x_start_chunk = (xpos)//self.size_chunk
            y_start_chunk = (ypos)//self.size_chunk
            x_end_chunk = (xpos + xscreen)//self.size_chunk
            y_end_chunk = (ypos + yscreen)//self.size_chunk

            for x in range(x_start_chunk, x_end_chunk + 1) :
                for y in range(y_start_chunk, y_end_chunk + 1) :
                    key = (x,y)
                    if key in self.dic_monster :
                        for monster in self.dic_monster[key] :
                            monster.move()
                            list_modif.append( (i, monster.name, monster.pos_x, monster.pos_y) )

        return list_modif