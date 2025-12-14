from serv.in_game.C_read_monster import Read_monster
import var #Fichier
import pygame
from serv.C_server import Server
import threading,numpy as np

class Server_game(Server) :
    """Contient tout le game = Mere. Update les particules"""
    def __init__(self,host='0.0.0.0', port=5000):

        super().__init__(host, port)  # <-- Appelle le constructeur de Server
        
        #self.canva_map = self.map_cell.canva
        self.is_running_game = True

        #self.lClient = None

        self.fps = var.FPS_CELL_UPDATE
        self.fpsClock = pygame.time.Clock()
        self.dt = 0 # Delta time between frames = devra faire *dt pour les mouvements   
           
        
    @classmethod
    def from_server(cls, server: "Server"):
        """Créer un Server_game à partir d’un Server existant"""
        new = cls(server.host, server.port)
        # Copier les infos du lobby
        new.lClient = server.lClient
        new.server = server.server
        new.nbr_player = server.nbr_player
        new.map_cell = server.map_cell
        new.buffers = server.buffers
        new.map_monster = server.map_monster
        new.is_running_menu=False
        new.is_running_game=True

        return new

    def loop_server_game(self):
        """Loop qui est effectué sur le serv pour update les cells"""
        while self.is_running_game :
            dt = self.fpsClock.tick(self.fps)/1000

            #for i in range(100):  #20 fps si pas les thread reception et envoie
            result_cell = self.map_cell.return_chg(self.lClient) #Mettre dt plus tard pour les particules
            #return_monster = self.map_monster.return_chg(self.lClient,self.map_cell.grid_type) #Mettre dt plus tard pour les monstres
            
            if len(result_cell[0]) != 1:
                self.send_data_update(result_cell,3)

            #if len(return_monster) != 0 :
            #    self.send_data_update(return_monster,4)
            self.handle_clients()

            fps = self.fpsClock.get_fps()
            #if fps < 220 : #Affiche le fps quand c'est critique
            #print(fps)

        print("End boucle loop_server_game")

    def init_canva(self):
        return self.map_cell.return_all(self.lClient) #Renvoie tout les pixels à dessiner
    
    def init_mobs(self):
        return self.map_monster.return_all_monster(self.lClient)

    def start_game(self):
        self.send_data_all([0]) #0 pour start game

        result_cell = self.init_canva()
        #result_monster = self.init_mobs()

        self.send_data_update(result_cell,3) #Envoie à tt le monde tout les nouveau pixels à draw
        #self.send_data_update(result_monster,5) #Envoie à tt le monde tout les nouveau pixels à draw

        threading.Thread(target=self.loop_server_game, daemon=True).start()