from serv.in_game_test.read_map_test import Read_map
import var #Fichier
import pygame
from serv.server import Server
import threading,numpy as np

class Server_game(Server) :
    """Contient tout le game = Mere. Update les particules"""
    def __init__(self,host='0.0.0.0', port=5000):

        super().__init__(host, port)  # <-- Appelle le constructeur de Server

        self.map = Read_map(var.bg)
        #self.canva_map = self.map.canva
        self.is_running_game = True

        #self.lClient = None
        self.lInfoClient = []
        self.fps = var.fps
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
            new.lClient[client]["screen_size"][0] = new.lClient[client]["screen_size"][0]//var.cell_size
            new.lClient[client]["screen_size"][1] = new.lClient[client]["screen_size"][1]//var.cell_size

        return new

    def loop_server_game(self):
        """Loop qui est effectué sur le serv pour update les cells"""
        while self.is_running_game :
            dt = self.fpsClock.tick(self.fps)/1000

            result = self.map.return_chg(self.lInfoClient)
            #print(result)


            if len(result[0]) != 1:
                #print("OK")
                self.send_data_update(result) #Envoie à tt le monde tout les nouveau pixels à draw
            
            fps = self.fpsClock.get_fps()
            if fps < 60 : #Affiche le fps quand c'est critique
                print(fps)

    def init_canva(self):

        self.lInfoClient = np.zeros((len(self.lClient), 4), dtype=np.int32)  # 4 colonnes : xpos, ypos, xscreen, yscreen

        for i,client in enumerate(self.lClient.keys()) :
            xpos,ypos = self.lClient[client]["position"]
            xscreen,yscreen = self.lClient[client]["screen_size"]
            self.lInfoClient[i,:] = [xpos,ypos,xscreen,yscreen]

        return self.map.return_all(self.lInfoClient) #Renvoie tout les pixels à dessiner
    
    def start_game(self):
        self.send_data_all({"id":"start game"})
        result = self.init_canva()
        #if result != [] :
        self.send_data_update(result) #Envoie à tt le monde tout les nouveau pixels à draw
        self.current_thread = threading.Thread(target=self.loop_server_game, daemon=True).start()