import pygame, threading, time
from client.core.state import State
from client.core.client import Client
from serv.core.server_game import Server_game
from shared.constants import fps,world

#from C_inGame import InGame
#from C_card import Card

class Main:
    """Class main = à on top le fichier main.py puis juste après le C_main"""
    def __init__(self):
        """Contient le screen = le truc affiché à l'écran / font = ecriture (Arial et tt), Client = class / State = class qui affiche"""
        # Set up the display (width, height)
        self.screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.RESIZABLE,pygame.FULLSCREEN | pygame.SCALED)
        self.screenSize = (self.screen.get_width(),self.screen.get_height())
        
        #ecriture
        self.font = pygame.font.SysFont(None, 48)

        #Set up the clock for managing the frame rate
        self.fps = fps.FPS_CLIENT
        self.fpsClock = pygame.time.Clock()
        self.dt = 0 # Delta time between frames = devra faire *dt pour les mouvements

        #self.Game = InGame(self.screen,self.screenSize,self.font,self.cards)
        self.Server = None
        self.objClicked = None

        self.client = Client(self.font,self.screen,self)
        self.state = State(self.screen,self.screenSize,self.font,self.client,world.CELL_SIZE)


    def run(self):
        """Ce qui est run à chaque itérations"""
        running = True
        while running:

            self.dt = self.fpsClock.tick(self.fps) / 1000 #à utiliser plus tard pour faire que si la personne tourne à moins de fps ou plus = va plus ou moins vite
            
            if self.state.mod == "game":
                self.key_event()

            for event in pygame.event.get():
                #Capture les events = touche /clique de la souris / clavier
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:

                    if self.state.mod == "game":
                        if event.key == pygame.K_p :
                            self.state.game.map.draw = not self.state.game.map.draw
                        
                    elif self.objClicked != None:

                        txt = self.objClicked.dicRect_input[self.objClicked.id+"_input"]["text"]

                        if event.key == pygame.K_RETURN:
                            self.state.mod = "loading"
                            print("Loading")
                            self.objClicked.dicRect_input[self.objClicked.id+"_input"]["text"] = txt.replace("|","")
                            threading.Thread(target = self.connect_serv).start()

                        elif event.key == pygame.K_ESCAPE:
                            self.objClicked.dicRect_input[self.objClicked.id+"_input"]["text"] = txt.replace("|","")
                            self.objClicked = None

                        elif event.key == pygame.K_BACKSPACE:
                            self.objClicked.dicRect_input[self.objClicked.id+"_input"]["text"] = txt[:-2] + "|"

                        else :
                            if len(txt) < 30: #max char
                                self.objClicked.dicRect_input[self.objClicked.id+"_input"]["text"] = txt[:-1] + str(event.unicode) + txt[-1]

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.state.mod=="game":
                        pass


                    elif self.state.mod == "menu":
                        if self.state.host.get_rect().collidepoint(event.pos):
                            #("Play button clicked")

                            self.state.show_ip.update_text("show_ip",f"Waiting for creation...")
                            self.state.start.update_text("start","...")
                            self.state.mod = "host"

                            threading.Thread(target = self.create_server_thread).start()

                        elif self.state.join.get_rect().collidepoint(event.pos):
                            print("join button clicked")
                            self.state.mod = "connexion"

                        elif self.state.quit.get_rect().collidepoint(event.pos):
                            #("Quit button clicked")
                            running = False

                    elif self.state.mod == "connexion":

                        if self.state.ip.get_rect().collidepoint(event.pos):

                            if self.objClicked == None:
                                self.state.ip.dicRect_input[self.state.ip.id+"_input"]["text"] += "|"
                                self.objClicked = self.state.ip

                        elif self.state.menu.get_rect().collidepoint(event.pos):
                            self.objClicked = None
                            self.state.ip.dicRect_input[self.state.ip.id+"_input"]["text"] = self.state.ip.dicRect_input[self.state.ip.id+"_input"]["text"].replace("|","")
                            self.state.mod = "menu"

                        elif self.state.connexion.get_rect().collidepoint(event.pos):
                            self.state.mod = "loading"
                            print("loading")
                            threading.Thread(target = self.connect_serv).start()

                        else :  #deselection
                            if self.objClicked != None:
                                self.state.ip.dicRect_input[self.objClicked.id+"_input"]["text"] = self.state.ip.dicRect_input[self.objClicked.id+"_input"]["text"].replace("|","")
                                self.objClicked = None

                    elif self.state.mod == "wait_serv":

                        if self.state.menu.get_rect().collidepoint(event.pos):
                            if self.client.connected is True :
                                self.client.connected = False
                                print("Connected = false")

                            self.state.mod = "menu"
                    
                    elif self.state.mod == "host":

                        if self.state.start.get_rect().collidepoint(event.pos) and self.client.connected :
                            #self.Server = Server_game.from_server(self.Server)

                            self.start_game()

                        elif self.state.menu.get_rect().collidepoint(event.pos):
                            
                            self.client.connected = False
                            self.state.mod = "menu"

                            if self.Server is not None:
                                self.Server.stop_server()
                                self.Server = None
                                self.state.add_alert("Serveur stoppé",)

            #Affiche ce qu'il doit être affiché en fonction du mode (reglage/menu/game)
            self.state.a_state(self.dt)

            if self.client.connected :
                self.client.poll_reception()

            self.handle_events()

            # Update le screen = sans sa l'ecran est pas mis a jour
            pygame.display.flip()


        pygame.quit()

    def start_game(self):

        threading.Thread(target=self.Server.start_game, daemon=True).start()

    def connect_serv(self):
        """Connecte au serveur"""
        self.state.mod = self.state.connexion_serv(self.client)  #Connexion serv
        self.objClicked = None

    def create_server_thread(self):
        """Crée le serveur dans un thread séparé"""
        self.Server = Server_game()
        ip,port = self.Server.start_server(self.client)

        self.client.connexion_serveur(ip_port =f"{ip}:{port}")

        self.state.show_ip.update_text("show_ip",f"ip:port = {ip}:{port}")
        self.state.start.update_text("start","Jouer")
        print("Create serv et connection!")

    def key_event(self):

        key = pygame.key.get_pressed()
        buttons = pygame.mouse.get_pressed()  #0:left/1:middle/2:right

        if key[pygame.K_z] :
            self.client.send_data(id=3,data=[0]) #lié au serveur les données/haut

        if key[pygame.K_s] :
            self.client.send_data(id=3,data=[1]) #lié au serveur les données/bas

        if key[pygame.K_q] :
            self.client.send_data(id=3,data=[2]) #lié au serveur les données/gauche

        if key[pygame.K_d] :
            self.client.send_data(id=3,data=[3]) #lié au serveur les données /right

        if buttons[0] : 

            #self.next_allowed_shot = now+self.rechargement/1000
            self.state.game.shot()
            #self.client.send_data(id=4,data=[self.])

        #if key[pygame.K_k] :
        #    self.client.send_data({"id":"dash"}) #futur dash (vitesse x), set vitesse y à 0

        #if key[pygame.K_SPACE] : #futur saut (vitesse y)
        #    self.client.send_data("id":"move", "deplacement":"jump") 

    def handle_events(self):

        events = self.state.game.player_command

        for input in events :

            if input == None:

                continue

            id = input[0]

            if id==4 :

                self.client.send_data(id=4,data=[input[1]])

        events.clear()