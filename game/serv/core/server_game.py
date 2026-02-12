from shared.constants import fps,world
import pygame
from serv.core.server import Server

class Server_game(Server) :
    """Contient tout le game = Mere. Update les particules"""
    def __init__(self):

        super().__init__()  # <-- Appelle le constructeur de Server
        
        #self.canva_map = self.map_cell.canva

        #self.lClient = None

        self.fps = fps.FPS_SERVER
        self.fpsClock = pygame.time.Clock()
        self.base_movement = world.RATIO
        self.dt = 0 # Delta time between frames = devra faire *dt pour les mouvements   

    def loop_server_game(self):
        """Loop qui est effectué sur le serv pour update les cells"""

        while self.is_running_game :
            dt = self.fpsClock.tick(self.fps)/1000

            #result_cell = self.map_cell.return_chg(self.lClient) #Mettre dt plus tard pour les particules
            return_monster = self.map_monster.return_chg(self.lClient,self.map_cell,dt) #Mettre dt plus tard pour les monstres
            result_projectile = self.projectile_manager.return_chg(self.lClient,dt,self.map_cell)

            #if len(result_cell[0]) != 1:
            #    self.send_data_update(result_cell,3)
            if len(return_monster[0]) != 0 :
                self.send_data_update(return_monster,4)

            if len(result_projectile)!= 0 :
                self.send_data_update(result_projectile[0],7)

                self.send_data_update(result_projectile[1],8)

                self.send_data_update(result_projectile[2],11)

            self.handle_clients()
            self.handle_player(dt)

            #if fps < 30 : #Affiche le fps quand c'est critique
            #    print(fps)

        print("End boucle loop_server_game")

    def handle_player(self,dt): #Player = key/input/le nain a l'écran quoi pas les msg

        for socket in self.lClient.keys():

            delta = self.lClient[socket].update_pos(self.map_cell,dt)
            
            #cell = self.map_cell.return_cells_delta(self.lClient[socket],self.convert_list_base(delta))

            #if cell != []:
            #    self.send_data([3,cell],socket)
            #self.send_data_all((6,self.lClient[socket].id,delta[0],delta[1]))
            if delta != (0,0):
                self.send_data_all((6,self.lClient[socket].id,self.lClient[socket].pos_x,self.lClient[socket].pos_y))

            if self.lClient[socket].send_new_life == True :
                life = self.lClient[socket].send_life()
                self.send_data((12,life),socket)
            
            if self.lClient[socket].send_new_money == True :
                money = self.lClient[socket].send_money()
                self.send_data((13,money), socket)
            
    def init_canva(self):
        return self.map_cell.return_all(self.lClient) #Renvoie tout les pixels à dessiner
    
    def init_mobs(self):
        return self.map_monster.return_all_monster(self.lClient)
    
    def init_weapon(self):

        for client in self.lClient.values():
            weapons_info = client.return_weapon_info()

            for weapon in weapons_info :

                self.send_data_all([10,weapon,client.id])
    
    def change_state(self):
        self.is_running_game = not self.is_running_game
        self.is_running_menu = not self.is_running_menu

    def start_game(self):
        print("start game")
        self.change_state()

        self.send_data_all([0]) #0 pour start game

        #result_cell = self.init_canva()
        result_monster = self.init_mobs()
        self.init_weapon()

        #print(result_monster)

        #self.send_data_update(result_cell,3) #Envoie à tt le monde tout les nouveau pixels à draw
        self.send_data_update(result_monster,5) #Envoie à tt le monde tout les nouveau monstres à draw

        self.send_data_all([9]) #9 : a fini de load

        self.loop_server_game()

    def convert_to_base(self,nbr):
        return nbr//self.base_movement
    
    def convert_list_base(self,list):
        return [self.convert_to_base(list[i]) for i in range(len(list))]

    def handle_shot(self,id_weapon,angle,sender):

        infos = self.lClient[sender].weapons.create_shot(id_weapon,self.lClient[sender].return_pos(),angle)

        if infos == None :
            return
        
        else :
            projectiles = infos

            self.lClient[sender].update_next_allowed_shot(id_weapon)
            #print("Next allowed shot = ",next_allowed_shot)

            for projectile in projectiles :


                self.projectile_manager.add_projectile_create(projectile)