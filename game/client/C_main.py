import pygame, threading
from client.state import State
from client.client import Client
from serv.server import Server
from client.events import event_queue
import var

#from C_inGame import InGame
#from C_card import Card

class Main:
    def __init__(self,size):
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
        self.objClicked = None

        self.mod = "menu" #menu/reglage/game

        self.client = Client(self.font,self.screen,self)
        self.state = State(self.screen,self.screenSize,self.font,self.client,size)


    def run(self):
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:

                    if self.objClicked != None:

                        txt = self.objClicked.dicRect[self.objClicked.id+"_input"]["text"]

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

                            self.state.show_ip.update_text("show_ip",f"ip:port = {self.client.ip}:{5000}")
                            self.state.start.update_text("start","Lancement du serveur...")
                            
                            self.Server = Server()
                            threading.Thread(target=self.Server.start_server, args = (5000,self.client)).start()
                            self.mod = "host"
                            
                            self.state.start.update_text("start","Serveur créé")
                            print("Create serv et connection!")

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

                        if self.state.start.rect.collidepoint(event.pos):
                            self.client.send_data({"id":"start game"})


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

            # Update the display
            pygame.display.flip()

            self.dt = self.fpsClock.tick(self.fps) / 1000

        pygame.quit()

    def perform_event_queue(self):
        """Traite les évenements globaux"""
        while not event_queue.empty():
            event = event_queue.get()
            if event["type"] == "SERVER_DISCONNECTED":
                self.state.add_alert("Déconnecté du serveur",5)

                self.mod = "menu"

    def connect_serv(self):
        self.mod = self.state.connexion_serv(self.client)  #Connexion serv
        self.objClicked = None