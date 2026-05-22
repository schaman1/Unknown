from serv.domain.mob import monster
from shared.constants.world import LEN_X_CHUNK,LEN_Y_CHUNK

class Read_monster :

    def __init__(self,width_chunk,height_chunk,base_movement) :

        self.dic_monster = {}
        #self.map_monster = pygame.image.load(filename_map_monster).convert()
        self.size_chunk_all = (LEN_Y_CHUNK,LEN_X_CHUNK)
        self.size_chunk = (height_chunk,width_chunk)

        self.base_movement = base_movement

        self.id = 0

        self.state_map = {"idle": 0, "moving": 1, "attacking": 2, "dead": 3,"run away":4,"loading":5}

        self.init_dic_monster()

    def generate_id(self):
        self.id = (self.id+1)%255
        return self.id

    def init_dic_monster(self) :

        for i in range(self.size_chunk_all[0]) :
            for j in range(self.size_chunk_all[1]) :
                self.dic_monster[i*self.base_movement+j] = []

        self.create_list_monster()

    def return_all_monster(self,lInfoClient) :

        list_modif = []
        for i in range(len(lInfoClient)):
            #list_modif.append({})
            list_modif.append([])
            for chunk in self.dic_monster :
                #list_modif[i] = []
                for monster in self.dic_monster[chunk] :

                    #state_id = self.state_map.get(monster.state, 0) #Why ? Always 0 by default
                    list_modif[i].append((chunk,monster.id, monster.pos_x, monster.pos_y, monster.name))

        return list_modif
    
    def create_monster(self,monster):
        
        monster.id = self.generate_id()
        chunk = self.return_chunk(monster.pos_x,monster.pos_y)
        self.dic_monster[chunk[0]*100+chunk[1]].append(monster)

    def create_list_monster(self) :

        self.create_monster(monster.Limace(3411,17300))
        self.create_monster(monster.Defendeur(30000,25000))
        self.create_monster(monster.Foulli(12000,15400))

        #for y in range(self.size_chunk_all[0]):
        #        for x in range(self.size_chunk_all[1]):
                    #color = self.map_monster.get_at((x, y))[:3]  # (r,g,b)

                    #if color == (0, 0, 0):      # pixel noir = skeleton
                        #print(f"Création d'un Skeleton en ({x}, {y})")
                    #if y==10 and x == 10 :
                        
        #            self.dic_monster[y//self.size_chunk_all[0]*100+x//self.size_chunk_all[1]].append(Skeleton(x*self.base_movement,y*self.base_movement,x*1000+y))

    def return_chg(self, lInfoClient, map,dt,collision_handler,projectile_manager) :
        """Itere parmis tout les monstres visibles et les move, renvoie une liste des modifs à faire"""

        list_modif = []

        list_chunk_client_see = self.return_list_chunk_client_see(lInfoClient,list_modif)

        list_monster_change_chunk = []

        for y in range(self.size_chunk_all[0]) :
            for x in range(self.size_chunk_all[1]) :

                chunk = y*100+x

                liste_client_see = self.return_client_see(x,y,list_chunk_client_see)
                if liste_client_see != [] :

                    #for monster in self.dic_monster[chunk] :
                    for i in range(len(self.dic_monster[chunk])-1,-1,-1):

                        monster = self.dic_monster[chunk][i]

                        monster.update(map,lInfoClient,dt,collision_handler,projectile_manager)

                        state_id = self.state_map.get(monster.state, 0)

                        for client_idx in liste_client_see :
                            list_modif[client_idx].append((chunk,monster.id, monster.pos_x, monster.pos_y, state_id))
                            #list_modif[client][chunk].append((monster.id, monster.pos_x, monster.pos_y))

                        new_chunk = self.return_chunk(monster.pos_x,monster.pos_y)
                        new_chunk = new_chunk[0]*self.base_movement+new_chunk[1]
                        if new_chunk != chunk:
                            list_monster_change_chunk.append([chunk,new_chunk,monster])
                            del self.dic_monster[chunk][i]

        for i in range(len(list_monster_change_chunk)) :
            old_chunk,new_chunk,monster = list_monster_change_chunk[i]
            self.dic_monster[new_chunk].append(monster)
            list_monster_change_chunk[i][2] = monster.id

        return list_modif,list_monster_change_chunk
    
    def init_list_modif_client(self,x_chunk,y_chunk,list_modif,i) :

        pass
        #for x in range(x_chunk - 2, x_chunk + 3) :
        #        for y in range(y_chunk - 2, y_chunk + 3) :
        #            chunk = x*100+y
        #            list_modif[i][chunk] = []

    def return_chunk(self,x,y):
        ys = (y//self.base_movement)//self.size_chunk[0]
        xs = (x//self.base_movement)//self.size_chunk[1]

        return ys,xs

    def return_list_chunk_client_see(self,lClient,list_modif) :

        list_chunk_client_see = []

        for i,client in enumerate(lClient.values()) :
            list_modif.append([])

            y_chunk,x_chunk = self.return_chunk(client.pos_x,client.pos_y)

            list_chunk_client_see.append([x_chunk,y_chunk])

            self.init_list_modif_client(x_chunk,y_chunk,list_modif,i)

        return list_chunk_client_see
    
    def return_client_see(self,x,y,list_chunk_client_see,vision:int = 1) :

        liste_client_see = []

        for i,e in enumerate(list_chunk_client_see) :

            #liste_client_see.append(i)

            x_chunk = e[0]
            y_chunk = e[1]

            if x_chunk - vision <= x <= x_chunk + vision and y_chunk - vision <= y <= y_chunk + vision :
                liste_client_see.append(i)

        return liste_client_see

