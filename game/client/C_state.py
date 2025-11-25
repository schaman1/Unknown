import pygame, threading
from client.rendering.texture import color
from client.C_button import Button
from client.C_alert import Alert
from client.C_load import Load
from client.C_game import Game
from client.Personnages_client.perso1 import Player

class State:
    """Class qui affiche tout"""

    def __init__(self,screen,screenSize,font,client,cell_size):
        """Contient tout les bouttons du menu a blit"""
        self.screen = screen
        self.Size = screenSize
        self.cell_size = cell_size
        self.font = font
        self.client = client
        self.load = Load(screen)

        self.player = Player("../assets/playerImg.png", 500, 500)
        self.posClient = (500,500)#A modifier après

        self.game = Game(cell_size,self.Size)

        self.join = Button(pygame.Rect(self.Size[0]/3, 2*self.Size[1]/18, self.Size[0]/3, self.Size[1]/6),color["GREEN"],"Rejoindre une partie",self.font,"join")
        self.host = Button(pygame.Rect(self.Size[0]/3, 7*self.Size[1]/18, self.Size[0]/3, self.Size[1]/6),color["GREY"],"Creer une partie",self.font,"host")
        self.quit = Button(pygame.Rect(self.Size[0]/3, 12*self.Size[1]/18, self.Size[0]/3, self.Size[1]/6),color["RED"],"Quit",self.font,"quit")

        self.ip = Button(pygame.Rect(self.Size[0]/3, 7*self.Size[1]/18, self.Size[0]/3, self.Size[1]/6),color["GREY"],"Ip:port",self.font,"ip")
        self.ip.create_input("RIGHT",color["BLACK"],"")
        self.connexion = Button(pygame.Rect(self.Size[0]/3, 2*self.Size[1]/18, self.Size[0]/3, self.Size[1]/6),color["GREEN"],"Se connecter",self.font,"connexion")

        self.start = Button(pygame.Rect(self.Size[0]/3, 2*self.Size[1]/18, self.Size[0]/3, self.Size[1]/6),color["GREEN"],"Lancer la partie",self.font,"start")
        self.show_ip = Button(pygame.Rect(self.Size[0]/3, 7*self.Size[1]/18, self.Size[0]/3, self.Size[1]/6),color["GREY"],"ip:port = ",self.font,"show_ip")

        self.menu = Button(pygame.Rect(self.Size[0]*2.5/6, 15.5*self.Size[1]/18, self.Size[0]/6, self.Size[1]/12),color["RED"],"Menu",self.font,"menu")
        self.alert = [] #L'ensemble des alertes qui doivent être affiché

        #dic boutton menu : 1= rect, 2=couleur, 3=texte
        self.dicMenu = {"join": self.join,
                        "host": self.host,
                        "quit": self.quit}
        
        self.dicConnexion = {"ip": self.ip,
                            "connexion": self.connexion,
                            "menu": self.menu}
        
        self.dicCreation = {"menu": self.menu,
                            "start": self.start,
                            "ip": self.show_ip}
        
        self.dicWaiting = {"menu": self.menu}
        
        self.no_black_screen = ""#"loading"

    def a_state(self,state):
        """Prend en param l'état / state et dessine en fct ce qu'il doit être dessiner"""

        if state not in self.no_black_screen:
            self.screen.fill(color["BLACK"])

        if state == "menu":
            
            for btn in self.dicMenu.values():

                btn.draw(self.screen)

            #test_vision(self.screen,self.Size)

        elif state == "game":

            x,y = self.return_pos_blit()
            self.game.draw(self.screen,x,y)

            #.drawAll()

        elif state == "wait_serv":
            
            for btn in self.dicWaiting.values():
                btn.draw(self.screen)

            self.draw_waiting()

        elif state == "connexion":

            for btn in self.dicConnexion.values():

                btn.draw(self.screen)

        elif state == "host":

            for btn in self.dicCreation.values():

                btn.draw(self.screen)

            self.client.display_clients_name()

        elif state == "loading":
            self.draw_load()

        else : 
            pass

        self.draw_alert()

    def return_pos_blit(self):   
        """
        renvoie la position (x, y) à blit du perso
        """
        #x = -self.posClient[0]*self.cell_size + self.Size[0]//2
        #y = -self.posClient[1]*self.cell_size + self.Size[1]//2
        x = -self.player.pos_x*self.cell_size + self.Size[0]//2
        y = -self.player.pos_y*self.cell_size + self.Size[1]//2
        return (x,y)

    def connexion_serv(self,client):
        """renvoie le mode de jeu apres connexion"""
        ip_port = self.ip.dicRect[self.ip.id+"_input"]["text"].replace("|","")

        self.start.update_text("start","Connexion...")
        client.connected = None
        threading.Thread(target=client.connexion_serveur, args=(ip_port,)).start()

        start_time = pygame.time.get_ticks()
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Temps écoulé en secondes

        while client.connected == None and elapsed_time < 15:  # Attendre la connexion ou un timeout de 5 secondes

            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            
            if client.connected : 
                print("En attente du serveur...")
                return "wait_serv"

        if client.err_message == "" :
            client.err_message = "Attente trop longue"
        self.alert.insert(0,Alert(self.screen,client.err_message,5))
        return "connexion"

    def draw_load(self):
        """Si appele, dessine les ronds qui tournent"""
        self.load.draw()

    def draw_waiting(self):
        """Draw cette ecran en attendant que le host lance la partie"""
        waiting_text = self.font.render("En attente d'autres joueurs...", True, color["WHITE"])
        text_rect = waiting_text.get_rect(center=(self.Size[0]//2, self.Size[1]//2))
        self.screen.blit(waiting_text, text_rect)

        self.client.display_clients_name()

    def draw_alert(self):
        """Dessine toutes les alert (ex : deconnection de serv) en haut de l'ecran"""

        for idx, warning in enumerate(self.alert):

            if warning.start_time < pygame.time.get_ticks() :
                self.alert.remove(warning)

                continue #Passe a l'iteratio  d'après

            warning.update_pos(idx)
            warning.draw()

    def add_alert(self,err_message,time=5):
        """prend en param le message et le temps de l'alert et l'insert dans les alert à dessiner à chaque iterations"""
        self.alert.insert(0,Alert(self.screen,err_message,time))


#def test_vision(screen,size):
#    light = pygame.Surface((size[0],size[1]), pygame.SRCALPHA)
#
#    light.fill((0,0,0))
#
#    for i in range(10):
#        pygame.draw.circle(light, (0,0,0,200 - (i+1)*20), (size[0]//2,size[1]//2), size[1]//3 - 2*i, width=0)
#
#    screen.blit(light,(0,0))
