from shared.constants import fps,world
import pygame,time,math
from serv.core.server import Server
from serv.config.add_objects_begin import OBJECTS

class Server_game(Server) :
    """Contient tout le game = Mere. Update les particules"""
    def __init__(self):

        super().__init__()  # <-- Appelle le constructeur de Server
        
        #self.canva_map = self.map_cell.canva

        #self.lClient = None

        self.fps = fps.FPS_SERVER
        self.fpsClock = pygame.time.Clock()
        self.base_movement = world.RATIO

        # Pour eviter le lag
        self.next_send_time = time.perf_counter()
        self.send_interval = 1 / fps.FPS_SEND_POS_CLIENT  # 0.05s

        self.dt = 0 # Delta time between frames = devra faire *dt pour les mouvements

    def loop_server_game(self):
        """Loop qui est effectué sur le serv pour update les cells"""

        self.add_elements_to_game()

        while self.is_running_game :
            dt = self.fpsClock.tick(self.fps)/1000

            should_send = False
            if self.next_send_time <= time.perf_counter():

                should_send = True
                while self.next_send_time <= time.perf_counter():
                    self.next_send_time += self.send_interval

            return_monster,monster_change_chunk = self.map_monster.return_chg(self.lClient,self.map_cell,dt,self.collision_handler,self.projectile_manager) #Mettre dt plus tard pour les monstres
            result_projectile = self.projectile_manager.return_chg(self.lClient,dt,self.map_cell)

            self.collision_handler.trigger_collision(self.map_monster.dic_monster,self.lClient,self.projectile_manager.dic_projectiles)
            if len(self.collision_handler.effect_send)!=0:
                self.send_data_all([14,self.collision_handler.effect_send])
                self.collision_handler.effect_send.clear()
            if len(self.collision_handler.die_send)!=0:
                self.send_data_all([18,self.collision_handler.die_send])
                self.collision_handler.die_send.clear()

            if len(return_monster)!=0 :
                if should_send :
                    self.send_data_update(return_monster,4)

            if len(monster_change_chunk)!=0:
                self.send_data_all((20,monster_change_chunk))

            if len(result_projectile)!= 0 :
                self.send_data_update(result_projectile[0],7)

                self.send_data_update(result_projectile[1],8)

                self.send_data_update(result_projectile[2],11)

            self.handle_clients()
            self.handle_player(dt,should_send)

            #if fps < 30 : #Affiche le fps quand c'est critique
            #    print(fps)

        print("End boucle loop_server_game")

    def handle_player(self,dt,should_send): #Player = key/input/le nain a l'écran quoi pas les msg

        for socket in self.lClient.keys():

            self.check_intro_stop(socket)

            delta = self.lClient[socket].update_pos(self.map_cell,dt,self.collision_handler)
            
            if should_send :
                self.send_data_all((6,self.lClient[socket].id,self.lClient[socket].pos_x,self.lClient[socket].pos_y))

            if self.lClient[socket].send_new_life == True :
                life,max_life,id_player = self.lClient[socket].send_life()
                self.send_data((12,(life,max_life,id_player)),socket)

            if self.lClient[socket].send_new_money == True :
                money = self.lClient[socket].send_money()
                self.send_data((13,money), socket)

    def check_intro_stop(self,sender):

        if self.lClient[sender].fct_to_do() == True :

            self.lClient[sender].pos_x,self.lClient[sender].pos_y = world.POS_RESET[0]*self.base_movement,world.POS_RESET[1]*self.base_movement
            self.send_data([19,None],sender)

    def init_canva(self):
        return self.map_cell.return_all(self.lClient) #Renvoie tout les pixels à dessiner
    
    def init_mobs(self):
        return self.map_monster.return_all_monster(self.lClient)
    
    def init_weapon(self):

        for socket,client in self.lClient.items():
            weapons_info = client.return_weapon_info()

            for weapon in weapons_info :

                self.send_data([10,weapon],socket)
    
    def change_state(self):
        self.is_running_game = not self.is_running_game
        self.is_running_menu = not self.is_running_menu

    def start_game(self):
        print("start intro")
        self.change_state()

        self.send_data_all([0]) #0 pour start game

        #result_cell = self.init_canva()
        result_monster = self.init_mobs()
        self.init_weapon()

        #print(result_monster)

        #self.send_data_update(result_cell,3) #Envoie à tt le monde tout les nouveau pixels à draw
        self.send_data_update(result_monster,5) #Envoie à tt le monde tout les nouveau monstres à draw


        pygame.time.wait(int(1.5*1000))
        self.send_data_all([9]) #9 : a fini de load

        print("Start game")
        self.loop_server_game()

    def convert_to_base(self,nbr):
        return nbr//self.base_movement
    
    def convert_list_base(self,list):
        return [self.convert_to_base(list[i]) for i in range(len(list))]

    def handle_shot(self,id_weapon,sender):

        infos = self.lClient[sender].shot(id_weapon)

        if infos == None :
            return
        
        else :
            projectiles = infos

            self.lClient[sender].update_next_allowed_shot(id_weapon)
            #print("Next allowed shot = ",next_allowed_shot)

            for projectile in projectiles :


                self.projectile_manager.add_projectile_create(projectile)

    def add_object(self,object_info):
        
        """Create object + id_categorie = id du sous type genre spell, id=1 -> = bdf / 40 = dash"""
        type = object_info[0]
        id_categorie = object_info[1]
        pos_x = object_info[2]
        pos_y = object_info[3]
        price= object_info[4]

        chunk = self.convert_to_chunk(pos_x,pos_y)

        id,ele = self.objects_manager.add_object(type,id_categorie,pos_x,pos_y,chunk,price)

        data = [15,[id,world.TYPE_OBJECT[type],ele.id_cat,pos_x,pos_y,chunk,ele.price]]

        self.send_data_all(data)

    def convert_to_chunk(self,pos_x,pos_y):

        chunk_x,chunk_y =  self.map_cell.return_chunk(pos_x//self.base_movement,pos_y//self.base_movement)

        return chunk_y*self.base_movement+chunk_x
        
    def add_elements_to_game(self):

        for el in OBJECTS : #OBJECTS come from the add_objects_begin

            self.add_object(el)

    def trigger(self,chunk,id,sender):
        
        res = self.objects_manager.trigger(chunk,id,self.lClient[sender])

        if res!=None:

            action,chunk,id,element = res

            if action=="AddToInventaire" :

                id_weapon = 0
                pos_spell = self.lClient[sender].weapons.add_spell(element.id_cat,id_weapon)

                self.send_data_all([16,chunk,id]) #Destroy

                self.send_data([17,id_weapon,element.id_cat,pos_spell],sender)

            elif action=="Heal":

                self.lClient[sender].heal_respawn(element)

            elif action=="UpgradeWeapon":

                info_weapon = self.lClient[sender].upgrade_size_weapon(element.id_cat)
                self.send_data_all([16,chunk,id]) #Destroy
                
                self.send_data([10,info_weapon],sender)

            elif action=="UpgradeLife":

                info_weapon = self.lClient[sender].add_life(element.power)
                self.send_data_all([16,chunk,id]) #Destroy
                
            elif action == "OpenChest":

                self.send_data_all([16,chunk,id]) #Destroy
                
                id,ele,type = self.objects_manager.spawn_random_spell(element.id_cat,chunk,element.pos_x,element.pos_y)
                #Spawn random object

                data = [15,[id,world.TYPE_OBJECT[type],ele.id_cat,ele.pos_x,ele.pos_y,chunk,ele.price]]
                self.send_data_all(data)

    def throw_spell(self,id_weapon,id_spell,sender):

        spell_id_type = self.lClient[sender].remove_spell(id_weapon,id_spell)

        pos = self.lClient[sender].return_pos()

        self.add_object(("SPELL",spell_id_type,pos[0],pos[1],0))

    def distance(self,posa,posb):

        dist = (posa[0]-posb[0])**2 + (posa[1]-posb[1])**2
        return math.sqrt(dist)

    def try_tp_to_boss(self):

        for client in self.lClient.values() :

            pnj_pos = world.POS_PNJ[0]*self.base_movement,world.POS_PNJ[1]*self.base_movement

            dist = self.distance((client.pos_x,client.pos_y),world.POS_PNJ)

            print(dist,world.DIST_TO_TP_BOSS*self.base_movement,client.pos_x,pnj_pos[0])

            if dist > world.DIST_TO_TP_BOSS*self.base_movement :

                return
        
        self.tp_to_boss()

    def tp_to_boss(self):

        for client in self.lClient.values() :

            boss_pos = world.POS_BOSS[0]*self.base_movement,world.POS_BOSS[1]*self.base_movement

            client.pos_x = boss_pos[0]
            client.pos_y = boss_pos[1]

    def player_finish_intro(self,sender):
        
        self.lClient[sender].set_finish_intro()