from serv.in_game_test.read_map_test import Read_map
import var #Fichier
import pygame

class Server_game :
    """Contient tout le game = Mere. Update les particules"""
    def __init__(self,serv_main):
        self.canva_size = var.serv_size
        self.serv = serv_main
        self.map = Read_map(var.bg,var.cell_size,self.canva_size)
        #self.canva_map = self.map.canva
        self.is_running_game = True

        self.fps = var.fps
        self.fpsClock = pygame.time.Clock()
        self.dt = 0 # Delta time between frames = devra faire *dt pour les mouvements

    def loop_server_game(self):
        """Loop qui est effectué sur le serv pour update les cells"""
        while self.is_running_game :
            dt = self.fpsClock.tick(self.fps)/1000

            result = self.return_chg()
            if result != []:
                #print("OK")
                self.serv.send_data_all({"id":"to change","updates":result}) #Envoie à tt le monde tout les nouveau pixels à draw
            
            fps = self.fpsClock.get_fps()
            if fps < 20 : #Affiche le fps quand c'est critique
                print(fps)

    def return_chg(self):
        """Renvoie une liste des x,y,color à blit"""
        return self.map.return_sand()
        #return self.map.return_map()

    def init_canva(self):
        #l = []
        #for e in self.map.grid:
        #    for el in e :
        #        if el != None :
        #            l.append((el.x,el.y,el.color))
        #return l
        return self.map.return_all() #Renvoie tout les pixels à dessiner