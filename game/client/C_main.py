import pygame, threading
from client.state import State
from client.client import Client
from serv.server_game import Server_game
from serv.server import Server
from client.events import event_queue
import var

#from C_inGame import InGame
#from C_card import Card

class Main:
    """Class main = à on top le fichier main.py puis juste après le C_main"""
    def __init__(self,cell_size):
        """Contient le screen = le truc affiché à l'écran / font = ecriture (Arial et tt), Client = class / State = class qui affiche"""
        # Set up the display (width, height)
        self.screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h),pygame.FULLSCREEN | pygame.SCALED)
        self.screenSize = (self.screen.get_width(),self.screen.get_height())

        #ecriture
        self.font = pygame.font.SysFont(None, 48)

        #Set up the clock for managing the frame rate
        self.fps = var.fps
        self.fpsClock = pygame.time.Clock()
        self.dt = 0 # Delta time between frames = devra faire *dt pour les mouvements

        #self.Game = InGame(self.screen,self.screenSize,self.font,self.cards)
        self.Server = None
        self.server_name = "Game1"

        self.mod = "menu" #menu/reglage/game

        self.client = Client(self.font,self.screen,self)
        self.state = State(self.screen,self.screenSize,self.font,self.client,cell_size)

    def run(self):
        """Ce qui est run à chaque itérations"""
        running = True
        while running:

            for event in pygame.event.get():
                #Capture les events = touche /clique de la souris / clavier
                if event.type == pygame.QUIT:
                    running = False

                #if event.type == pygame.KEYDOWN:

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.mod == "menu":
                        if self.state.host.rect.collidepoint(event.pos):
                            #("Play button clicked")
                            self.Server = Server(var.intervalle_refresh_server_available,port = var.port, server_name = self.server_name)
                            threading.Thread(target=self.Server.start_server, args = (self.client,)).start()
                            threading.Thread(target=self.wait_serv_created).start()

                            self.state.game_name.update_text("game_name",f"Game : {self.Server.server_name}")
                            self.state.start.update_text("start","Lancement du serveur...")
                            self.mod = "host"
                            
                            
                            print("Create serv et connection!")

                        elif self.state.join.rect.collidepoint(event.pos):
                            print("join button clicked")
                            self.mod = "connexion"
                            threading.Thread(target = self.client.loop_reception_server_open).start()

                        elif self.state.quit.rect.collidepoint(event.pos):
                            #("Quit button clicked")
                            running = False

                    elif self.mod == "connexion":

                        if self.state.menu.rect.collidepoint(event.pos):
                            self.objClicked = None
                            self.mod = "menu"

                        elif self.state.connexion.rect.collidepoint(event.pos):
                            self.mod = "loading"
                            print("loading")
                            threading.Thread(target = self.connect_serv).start()
                            
                        for ip_port,btn in self.state.server_dispo.items():
                            if btn.rect.collidepoint(event.pos):
                                self.mod = "loading"
                                print("loading")
                                threading.Thread(target = self.connect_serv, args=(ip_port,)).start()

                    elif self.mod == "wait_serv":

                        if self.state.menu.rect.collidepoint(event.pos):
                            if self.client.connected is True :
                                self.client.connected = False
                                print("Connected = false")

                            self.mod = "menu"
                    
                    elif self.mod == "host":

                        if self.state.start.rect.collidepoint(event.pos):
                            self.Server = Server_game.from_server(self.Server)
                            self.client.send_data({"id":"start game"})
                            self.Server.start_game()

                        elif self.state.menu.rect.collidepoint(event.pos):
                            if self.Server is not None:
                                self.Server.stop_server()
                                self.Server = None
                                self.state.add_alert("Serveur stoppé",)

                            self.mod = "menu"
                            self.client.connected = False

                        #if self.state.play.rect.collidepoint(event.pos):
                            #self.mod = "game"
                            #threading.Thread(target=self.client.connexion_serveur, args=("localhost", 5000)).start()                           


            self.perform_event_queue()

            #Affiche ce qu'il doit être affiché en fonction du mode (reglage/menu/game)
            self.state.a_state(self.mod)

            # Update le screen = sans sa l'ecran est pas mis a jour
            pygame.display.flip()

            self.dt = self.fpsClock.tick(self.fps) / 1000 #à utiliser plus tard pour faire que si la personne tourne à moins de fps ou plus = va plus ou moins vite

        pygame.quit()

    def perform_event_queue(self):
        """Traite les évenements globaux"""
        while not event_queue.empty():
            event = event_queue.get()
            if event["type"] == "SERVER_DISCONNECTED":
                self.state.add_alert("Déconnecté du serveur",5)

                self.mod = "menu"

    def connect_serv(self,ip_port):
        """Connecte au serveur"""
        self.mod = self.state.connexion_serv(self.client,ip_port)  #Connexion serv
        self.objClicked = None

    def wait_serv_created(self):
        while True :
            if self.Server.is_running_menu :
                self.state.start.update_text("start","Jouer")
                return