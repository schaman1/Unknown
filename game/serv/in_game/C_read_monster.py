import pygame
from serv.in_game.C_monster import Skeleton

class Read_monster :

    def __init__(self,filename_map_monster,size_chunk,cell_dur,cell_vide,cell_liquid) :

        self.dic_monster = {}
        self.map_monster = pygame.image.load(filename_map_monster).convert()
        self.width, self.height = self.map_monster.get_size()
        self.size_chunk = size_chunk

        self.cell_dur = cell_dur
        self.cell_vide = cell_vide
        self.cell_liquid = cell_liquid


        self.init_dic_monster()

    def init_dic_monster(self) :

        for i in range(self.width//self.size_chunk+1) :
            for j in range(self.height//self.size_chunk+1) :
                self.dic_monster[f"{i},{j}"] = []

        self.create_list_monster()

    def return_all_monster(self,lInfoClient) :

        list_modif = []
        for i in range(len(lInfoClient)):
            list_modif.append({})
            for key in self.dic_monster :
                list_modif[i][key] = []
                for monster in self.dic_monster[key] :
                    list_modif[i][key].append((monster.id, monster.pos_x, monster.pos_y, monster.name))

        return list_modif

    def create_list_monster(self) :
        for x in range(self.width):
                for y in range(self.height):
                    color = self.map_monster.get_at((x, y))[:3]  # (r,g,b)

                    if color == (0, 0, 0):      # pixel noir = skeleton
                        #print(f"Création d'un Skeleton en ({x}, {y})")
                        self.dic_monster[f"{x//self.size_chunk},{y//self.size_chunk}"].append(Skeleton(x,y,f"{x},{y}"))


    def return_chg(self, lInfoClient, cells_arr) :
        """Itere parmis tout les monstres visibles et les move, renvoie une liste des modifs à faire"""

        list_modif = []

        list_chunk_client_see = self.return_list_chunk_client_see(lInfoClient,list_modif)

        for x in range(self.width//self.size_chunk+1) :
            for y in range(self.height//self.size_chunk+1) :

                chunk = f'{x},{y}'

                liste_client_see = self.return_client_see(x,y,list_chunk_client_see)
                if liste_client_see != [] :

                    for monster in self.dic_monster[chunk] :

                        monster.move(cells_arr,self.cell_dur,self.cell_vide,self.cell_liquid)

                        for client in liste_client_see :
                            list_modif[client][chunk].append((monster.id, monster.pos_x, monster.pos_y))

        return list_modif
    
    def init_list_modif_client(self,x_chunk,y_chunk,list_modif,i) :

        for x in range(x_chunk - 2, x_chunk + 3) :
                for y in range(y_chunk - 2, y_chunk + 3) :
                    chunk = f"{x},{y}"
                    list_modif[i][chunk] = []
    
    def return_list_chunk_client_see(self,lInfoClient,list_modif) :

        list_chunk_client_see = []

        for i,info in enumerate(lInfoClient) :
            list_modif.append({})

            xpos = info[0]
            ypos = info[1]

            x_chunk = xpos // self.size_chunk
            y_chunk = ypos // self.size_chunk

            list_chunk_client_see.append([x_chunk,y_chunk])

            self.init_list_modif_client(x_chunk,y_chunk,list_modif,i)

        return list_chunk_client_see
    
    def return_client_see(self,x,y,list_chunk_client_see,vision:int = 1) :

        liste_client_see = []

        for i,e in enumerate(list_chunk_client_see) :
            x_chunk = e[0]
            y_chunk = e[1]

            if x_chunk - vision <= x <= x_chunk + vision and y_chunk - vision <= y <= y_chunk + vision :
                liste_client_see.append(i)

        return liste_client_see

