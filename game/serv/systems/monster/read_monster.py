from serv.domain.mob import monster
from shared.constants.world import LEN_X_CHUNK,LEN_Y_CHUNK
from serv.config.position_all_monsters import MONSTER_POSITION

class Read_monster :

    def __init__(self,width_chunk,height_chunk,base_movement) :

        self.dic_monster = {}
        self.friendly_monsters = {}
        #self.map_monster = pygame.image.load(filename_map_monster).convert()
        self.size_chunk_all = (LEN_Y_CHUNK,LEN_X_CHUNK)
        self.size_chunk = (height_chunk,width_chunk)

        self.base_movement = base_movement

        self.direction = {"right":0,"left":1}

        self.id = 0

        #Monstres invoqués en cours de partie (ex: par le boss), à envoyer au client (msg 5)
        self.monster_to_create_send = []

        self.state_map = {"idle": 0, "moving": 1, "attacking": 2, "dead": 3,"run away":4,"loading":5}

        self.init_dic_monster()

    def generate_id(self):
        self.id = (self.id+1)%255
        return self.id

    def init_dic_monster(self) :

        for i in range(self.size_chunk_all[0]) :
            for j in range(self.size_chunk_all[1]) :
                self.dic_monster[i*self.base_movement+j] = []
                self.friendly_monsters[i*self.base_movement+j] = []

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

                    list_modif[i].append((chunk,monster.id, monster.pos_x, monster.pos_y, monster.name,self.direction[monster.side]))

        return list_modif
    
    def create_monster(self,monster,dest = None):
        if dest == None:
            dest = self.dic_monster
        
        monster.id = self.generate_id()
        monster.pos_y -= monster.half_height
        chunk = self.return_chunk(monster.pos_x,monster.pos_y)
        dest[chunk[0]*100+chunk[1]].append(monster)
        return chunk[0]*100+chunk[1]

    def spawn_minion(self,monster,dest= None):
        """Crée un monstre en cours de partie (invoqué par un boss) et prépare son envoi au client."""
        chunk = self.create_monster(monster,dest)
        self.monster_to_create_send.append((chunk,monster.id,int(monster.pos_x),int(monster.pos_y),monster.name,self.direction[monster.side]))

    def create_list_monster(self) :

        for name in MONSTER_POSITION.keys() :

            for pos in MONSTER_POSITION[name] :

                class_monster = None

                if name == "Laseroide" :
                    class_monster = monster.Laseroide

                elif name == "Limace" :
                    class_monster = monster.Limace

                elif name == "Escargot" :
                    class_monster = monster.Escargot

                elif name == "Foulli" :
                    class_monster = monster.Foulli

                elif name == "Defendeur" :
                    class_monster = monster.Defendeur

                elif name == "Skeleton" :
                    class_monster = monster.Skeleton

                if class_monster != None :

                    self.create_monster(class_monster(pos[0],pos[1]))

    def return_chg(self, lInfoClient, map,dt,collision_handler,projectile_manager) :
        """Itere parmis tout les monstres visibles et les move, renvoie une liste des modifs à faire"""

        list_modif = []

        list_chunk_client_see = self.return_list_chunk_client_see(lInfoClient,list_modif)

        list_monster_change_chunk = []

        list_minion_to_spawn = []

        list_monster_destroy = []

        for y in range(self.size_chunk_all[0]) :
            for x in range(self.size_chunk_all[1]) :

                chunk = y*100+x

                liste_client_see = self.return_client_see(x,y,list_chunk_client_see)
                if liste_client_see != [] :

                    #for monster in self.dic_monster[chunk] :
                    for i in range(len(self.dic_monster[chunk])-1,-1,-1):

                        monster = self.dic_monster[chunk][i]
                        monster.update(map,lInfoClient,dt,collision_handler,projectile_manager)

                        #Récupère les monstres invoqués par ce monstre (ex: le boss)
                        to_spawn = getattr(monster,"monsters_to_spawn",None)
                        if to_spawn :
                            list_minion_to_spawn.extend(to_spawn)
                            to_spawn.clear()

                        state_id = self.state_map.get(monster.state, 0)

                        for client_idx in liste_client_see :
                            
                            list_modif[client_idx].append((chunk,monster.id, monster.pos_x, monster.pos_y, state_id,self.direction[monster.side]))
                            #list_modif[client][chunk].append((monster.id, monster.pos_x, monster.pos_y))

                        new_chunk = self.return_chunk(monster.pos_x,monster.pos_y)
                        new_chunk = new_chunk[0]*self.base_movement+new_chunk[1]
                        if new_chunk != chunk:
                            list_monster_change_chunk.append([chunk,new_chunk,monster,False])
                            del self.dic_monster[chunk][i]
                        
                    for i in range(len(self.friendly_monsters[chunk])-1,-1,-1):
                        
                        monster = self.friendly_monsters[chunk][i]
                        monster.update(map,lInfoClient,dt,collision_handler,projectile_manager)
                        #print("Has update")
                        state_id = self.state_map.get(monster.state, 0)

                        for client_idx in liste_client_see :
                            
                            list_modif[client_idx].append((chunk,monster.id, monster.pos_x, monster.pos_y, state_id,self.direction[monster.side]))
                            #list_modif[client][chunk].append((monster.id, monster.pos_x, monster.pos_y))

                        if monster.has_to_destroy() :
                            list_monster_destroy.append((chunk,monster.id))
                            del self.friendly_monsters[chunk][i]
                        
                        else :
                            new_chunk = self.return_chunk(monster.pos_x,monster.pos_y)
                            new_chunk = new_chunk[0]*self.base_movement+new_chunk[1]
                            if new_chunk != chunk:
                                list_monster_change_chunk.append([chunk,new_chunk,monster,True])
                                del self.friendly_monsters[chunk][i]


        for i in range(len(list_monster_change_chunk)) :
            old_chunk,new_chunk,monster,friendly = list_monster_change_chunk[i]
            
            if friendly :
                self.friendly_monsters[new_chunk].append(monster)
            else :
                self.dic_monster[new_chunk].append(monster)
            list_monster_change_chunk[i][2] = monster.id

        #Enregistre les monstres invoqués cette frame (les place dans un chunk + leur donne un id)
        for minion in list_minion_to_spawn :
            self.spawn_minion(minion)

        return list_modif,list_monster_change_chunk,list_monster_destroy
    
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

    def spawn_monsters_from_l(self,monsters):

        for info_monster in monsters :

            id,hp,pos = info_monster

            if id == 42:
                monster_create = monster.Wall(pos[0],pos[1])
                monster_create.hp = hp
                self.spawn_minion(monster_create,self.friendly_monsters)