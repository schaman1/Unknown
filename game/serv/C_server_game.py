from serv.in_game.C_read_map import Read_map
from serv.in_game.C_read_monster import Read_monster
import var #Fichier
import pygame
from serv.C_server import Server
import threading,numpy as np

class Server_game(Server) :
    """Contient tout le game = Mere. Update les particules"""
    def __init__(self,host='0.0.0.0', port=5000):

        super().__init__(host, port)  # <-- Appelle le constructeur de Server

        self.map_cell = Read_map(var.BG_CELL)
        self.map_monster = Read_monster(var.BG_MONSTER,var.SIZE_CHUNK_MONSTER)
        #self.canva_map = self.map_cell.canva
        self.is_running_game = True

        #self.lClient = None
        self.lInfoClient = []
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

        for client in new.lClient.keys():
            #Met les screen_size à la bonne échelle
            new.lClient[client]["screen_size"][0] = new.lClient[client]["screen_size"][0]//var.CELL_SIZE + var.PADDING_CANVA
            new.lClient[client]["screen_size"][1] = new.lClient[client]["screen_size"][1]//var.CELL_SIZE + var.PADDING_CANVA
        return new

    def loop_server_game(self):
        """Loop qui est effectué sur le serv pour update les cells"""
        while self.is_running_game :
            dt = self.fpsClock.tick(self.fps)/1000

            result_cell = self.map_cell.return_chg(self.lInfoClient) #Mettre dt plus tard pour les particules
            return_monster = self.map_monster.return_chg(self.lInfoClient) #Mettre dt plus tard pour les monstres
            
            if len(result_cell[0]) != 1:
                self.send_data_update(result_cell,"to change cell") #Envoie à tt le monde tout les nouveau pixels à draw

            if len(return_monster) != 0 :
                self.send_data_update(return_monster, "to change monster")

            fps = self.fpsClock.get_fps()
            if fps < 60 : #Affiche le fps quand c'est critique
                print(fps)

    def init_canva(self):

        self.lInfoClient = np.zeros((len(self.lClient), 4), dtype=np.int32)  # 4 colonnes : xpos, ypos, xscreen, yscreen

        for i,client in enumerate(self.lClient.keys()) :
            xpos,ypos = self.lClient[client]["position"]
            xscreen,yscreen = self.lClient[client]["screen_size"]
            self.lInfoClient[i,:] = [xpos,ypos,xscreen,yscreen]

        return self.map_cell.return_all(self.lInfoClient) #Renvoie tout les pixels à dessiner
    
    def init_mobs(self):
        return self.map_monster.return_all_monster(self.lInfoClient)

    def start_game(self):
        self.send_data_all({"id":"start game"})

        result_cell = self.init_canva()
        result_monster = self.init_mobs()

        self.send_data_update(result_cell,"to change cell") #Envoie à tt le monde tout les nouveau pixels à draw
        self.send_data_update(result_monster,"set all monster") #Envoie à tt le monde tout les nouveau pixels à draw

        self.current_thread = threading.Thread(target=self.loop_server_game, daemon=True).start()