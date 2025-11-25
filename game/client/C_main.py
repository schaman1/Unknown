import pygame, threading
from client.C_state import State
from client.C_client import Client
from serv.C_server_game import Server_game
from serv.C_server import Server
from client.events import event_queue
from Personnages_client.perso1 import Player
import var

#from C_inGame import InGame
#from C_card import Card

class Main:
    """Class main = à on top le fichier main.py puis juste après le C_main"""
    def __init__(self):
        """Contient le screen = le truc affiché à l'écran / font = ecriture (Arial et tt), Client = class / State = class qui affiche"""
        # Set up the display (width, height)
        self.screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h),pygame.FULLSCREEN | pygame.SCALED)
        self.screenSize = (self.screen.get_width(),self.screen.get_height())

        #ecriture
        self.font = pygame.font.SysFont(None, 48)

        #Set up the clock for managing the frame rate
        self.fps = var.FPS_CLIENT
        self.fpsClock = pygame.time.Clock()
        self.dt = 0 # Delta time between frames = devra faire *dt pour les mouvements

        #self.Game = InGame(self.screen,self.screenSize,self.font,self.cards)
        self.Server = None
        self.objClicked = None

        self.mod = "menu" #menu/reglage/game

        self.client = Client(self.font,self.screen,self)
        self.state = State(self.screen,self.screenSize,self.font,self.client,var.CELL_SIZE)


    def run(self):
        """Ce qui est run à chaque itérations"""
        running = True
        while running:

            for event in pygame.event.get():
                #Capture les events = touche /clique de la souris / clavier
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:

                    if self.mod == "game":

                        if event.key == pygame.K_ESCAPE:
                            pass



                    elif self.objClicked != None:

                        txt = self.objClicked.dicRect[self.objClicked.id+"_input"]["text"]

                        self.state.player.pos_x +=1

                        if event.key == pygame.K_RETURN:
                            self.mod = "loading"
                            print("Loading")
                            self.objClicked.dicRect[self.objClicked.id+"_input"]["text"] = txt.replace("|","")
                            threading.Thread(target = self.connect_serv).start()

                        elif event.key == pygame.K_ESCAPE:
                            self.objClicked.dicRect[self.objClicked.id+"_input"]["text"] = txt.replace("|","")
                            self.objClicked = None

                        elif event.key == pygame.K_BACKSPACE:
                            self.objClicked.dicRect[self.objClicked.id+"_input"]["text"] = txt[:-2] + "|"

                        else :
                            if len(txt) < 30: #max char
                                self.objClicked.dicRect[self.objClicked.id+"_input"]["text"] = txt[:-1] + str(event.unicode) + txt[-1]

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.mod == "menu":
                        if self.state.host.rect.collidepoint(event.pos):
                            #("Play button clicked")

                            self.state.show_ip.update_text("show_ip",f"Waiting for creation...")
                            self.state.start.update_text("start","...")
                            self.mod = "host"

                            threading.Thread(target = self.create_server_thread).start()

                        elif self.state.join.rect.collidepoint(event.pos):
                            print("join button clicked")
                            self.mod = "connexion"

                        elif self.state.quit.rect.collidepoint(event.pos):
                            #("Quit button clicked")
                            running = False

                    elif self.mod == "connexion":

                        if self.state.ip.rect.collidepoint(event.pos):

                            if self.objClicked == None:
                                self.state.ip.dicRect[self.state.ip.id+"_input"]["text"] += "|"
                                self.objClicked = self.state.ip

                        elif self.state.menu.rect.collidepoint(event.pos):
                            self.objClicked = None
                            self.state.ip.dicRect[self.state.ip.id+"_input"]["text"] = self.state.ip.dicRect[self.state.ip.id+"_input"]["text"].replace("|","")
                            self.mod = "menu"

                        elif self.state.connexion.rect.collidepoint(event.pos):
                            self.mod = "loading"
                            print("loading")
                            threading.Thread(target = self.connect_serv).start()

                        else :  #deselection
                            if self.objClicked != None:
                                self.state.ip.dicRect[self.objClicked.id+"_input"]["text"] = self.state.ip.dicRect[self.objClicked.id+"_input"]["text"].replace("|","")
                                self.objClicked = None

                    elif self.mod == "wait_serv":

                        if self.state.menu.rect.collidepoint(event.pos):
                            if self.client.connected is True :
                                self.client.connected = False
                                print("Connected = false")

                            self.mod = "menu"
                    
                    elif self.mod == "host":

                        if self.state.start.rect.collidepoint(event.pos) and self.client.connected :
                            self.Server = Server_game.from_server(self.Server)
                            self.client.send_data({"id":"start game"})
                            self.Server.start_game()


                        elif self.state.menu.rect.collidepoint(event.pos):
                            
                            self.client.connected = False
                            self.mod = "menu"

                            if self.Server is not None:
                                self.Server.stop_server()
                                self.Server = None
                                self.state.add_alert("Serveur stoppé",)


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

    def connect_serv(self):
        """Connecte au serveur"""
        self.mod = self.state.connexion_serv(self.client)  #Connexion serv
        self.objClicked = None

    def create_server_thread(self):
        """Crée le serveur dans un thread séparé"""
        self.Server = Server(port = var.PORT)
        ip,port = self.Server.start_server(self.client)

        self.client.connexion_serveur(ip_port =f"{ip}:{port}")

        self.state.show_ip.update_text("show_ip",f"ip:port = {ip}:{port}")
        self.state.start.update_text("start","Jouer")
        print("Create serv et connection!")