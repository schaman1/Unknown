import pygame, threading
from assets.rendering.texture import color
from client.ui.button import Button
from client.ui.PopupManager.alert import Alert
from client.ui.load import Load
from client.core.game import Game
from client.config import assets

class State:
    """Class qui affiche tout"""

    def __init__(self,screen,screenSize,font,client,cell_size):
        """Contient tout les bouttons du menu a blit"""
        self.screen = screen
        self.Size = screenSize
        self.cell_size = cell_size
        self.font = font
        self.client = client
        self.mod = "menu"

        self.load = Load(screen)

        self.game = Game(cell_size, screenSize)

        self.join = Button((self.Size[0]/2, self.Size[1]/5), (self.Size[0]/3, self.Size[1]/6),assets.BTN,assets.BTN_HOVER,"Rejoindre une partie",self.font,"join")
        self.host = Button((self.Size[0]/2, 2.5*self.Size[1]/5), (self.Size[0]/3, self.Size[1]/6),assets.BTN,assets.BTN_HOVER,"Creer une partie",self.font,"host")
        self.quit = Button((self.Size[0]/2, 4*self.Size[1]/5), (self.Size[0]/3, self.Size[1]/6),assets.BTN,assets.BTN_HOVER,"Quit",self.font,"quit")

        self.ip = Button((self.Size[0]/2, 2.5*self.Size[1]/5), (self.Size[0]/3, self.Size[1]/6),assets.BTN,assets.BTN_HOVER,"Ip",self.font,"ip")
        self.ip.create_input("RIGHT",color["BLACK"],"",20)
        self.connexion = Button((self.Size[0]/2, self.Size[1]/5), (self.Size[0]/3, self.Size[1]/6),assets.BTN,assets.BTN_HOVER,"Se connecter",self.font,"connexion")

        self.start = Button((self.Size[0]/2, self.Size[1]/5), (self.Size[0]/3, self.Size[1]/6),assets.BTN,assets.BTN_HOVER,"Lancer la partie",self.font,"start")
        self.show_ip = Button((self.Size[0]/2, 2.5*self.Size[1]/5), (self.Size[0]/3, self.Size[1]/6),assets.BTN,assets.BTN_HOVER,"Ip = ",self.font,"show_ip")

        self.menu = Button((self.Size[0]/2, 4*self.Size[1]/5), (self.Size[0]/6, self.Size[1]/12),assets.BTN,assets.BTN_HOVER,"Menu",self.font,"menu")
        self.alert = [] #L'ensemble des alertes qui doivent être affiché

        #self.map_btn = Button((self.Size[0], 0), (self.Size[0]/10, self.Size[1]/20),assets.BTN,assets.BTN_HOVER,"MAP",self.font,"map","topright")

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

        #self.dicGame = {"map":self.map_btn}
        
        self.no_black_screen = ""#"loading"

    def a_state(self,dt):
        """Prend en param l'état / self.mod et dessine en fct ce qu'il doit être dessiner"""

        #if self.mod not in self.no_black_screen:
            #self.screen.fill(color["BLACK"])
        mouse_pos = pygame.mouse.get_pos()

        if self.mod == "game":

            x,y = self.return_pos_blit()
            self.game.draw(self.screen,x,y,dt,mouse_pos)

            #self.draw_btn(self.dicGame,mouse_pos)

        else :

            self.screen.fill(color["BLACK"])

            if self.mod == "menu":

                self.draw_btn(self.dicMenu,mouse_pos)

                #.drawAll()

            elif self.mod == "wait_serv":
                
                self.draw_btn(self.dicWaiting,mouse_pos)

                self.draw_waiting()

            elif self.mod == "connexion":

                self.draw_btn(self.dicConnexion,mouse_pos)

            elif self.mod == "host":

                self.draw_btn(self.dicCreation,mouse_pos)

                self.client.display_clients_name()

            elif self.mod == "loading":
                self.draw_load()

            elif self.mod == "intro start":
                self.game.draw_intro_start(self.screen)

            elif self.mod == "intro end":

                #En fonction de ce que tu fais mais la comme ça, si tu fais du fondu, les persos sont déjà désinné
                x,y = self.return_pos_blit()
                self.game.draw(self.screen,x,y,dt, mouse_pos)

                finish = self.game.draw_intro_end(self.screen)

                if finish :
                    self.mod = "game"


            else : 
                print("Unknown self.mod")

        self.draw_alert()

    def return_pos_blit(self):   
        """
        renvoie la position (x, y) à blit du background
        On bouge le background à la place du perso, pour les salles
        """
        #x = -self.posClient[0]*self.cell_size + self.Size[0]//2
        #y = -self.posClient[1]*self.cell_size + self.Size[1]//2
        client_id = self.game.player_all.client_id
        x = -self.game.player_all.dic_players[client_id].pos_x + self.Size[0]//2
        y = -self.game.player_all.dic_players[client_id].pos_y + self.Size[1]//2
        return (x,y)

    def connexion_serv(self,client):
        """renvoie le mode de jeu apres connexion"""
        ip_port = self.ip.dicRect_input[self.ip.id+"_input"]["text"].replace("|","")

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

    def draw_btn(self,dic:dict,mouse_pos):

        for btn in dic.values():
            btn.draw(self.screen,mouse_pos)



#def test_vision(screen,size):
#    light = pygame.Surface((size[0],size[1]), pygame.SRCALPHA)
#
#    light.fill((0,0,0))
#
#    for i in range(10):
#        pygame.draw.circle(light, (0,0,0,200 - (i+1)*20), (size[0]//2,size[1]//2), size[1]//3 - 2*i, width=0)
#
#    screen.blit(light,(0,0))
