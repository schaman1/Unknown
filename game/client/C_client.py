import socket, json, threading
import time
from client.events import event_queue

class Client:
    """Class client, traite les envoies de données et les receptions avec le serv"""
    def __init__(self, font,screen,main,ip="localhost", port=5000):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = None
        self.main = main

        self.id = "Coming soon"
        self.err_message = ""

        self.font = font
        self.screen = screen
        self.screen_size = self.screen.get_size()

    def return_ip_ngrok(self,ip_port):
        """Quand on se connnecte, ecrit ip;port = ici, les séparts"""
        try :
            ipshort, port = ip_port.split(":")
            ip = f"{ipshort}.tcp.eu.ngrok.io"
            port = port
            print(ip,port)
            return ip, int(port)

        except ValueError:
            return None, None
        
    def connexion_serveur(self, ip_port="localhost:5000"):
        "Create the client and connect to ther serveur"

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #-------- Pour ngrok = Online² --------
        #ip, port = self.return_ip_ngrok(ip_port)

        #-------- Pour local = LAN --------
        ip, port = ip_port.split(":")
        #ip = ip.strip()
        port = int(port) #Has to be an integer

        if ip is None or port is None:
            return self.return_err("Utilisez le format ip:port")
        #Créer le socket

        for essais in range(3): #Test 3 fois de se connecter 
            try:
                print(f"Tentative de connexion {essais+1}/3...")
                self.client.connect((ip, port)) #Ici connection 
                self.connection_succes()
                return
            except Exception as e:
                print(f"Échec connexion ({e}) — nouvelle tentative…")
                time.sleep(0.2)

        self.return_err("Ip ou port incorrect")

    def return_err(self,mess):
        #Va  changer err_message = dans une autre boucle teste si err message a change eet si a change = blit(alert)
        print(mess)
        self.err_message = mess
        self.connected = False

    def connection_succes(self):
        """Ici, lancé quand connection réussite = lance un thread = script qui va tourner à côté = reception serveurs"""
        print("Connecté au serveur")
        self.connected = True
        threading.Thread(target=self.loop_reception_server, daemon=True).start()

        self.send_data({"id":"new client connection","screen_size":self.screen_size})

    def loop_reception_server(self):
        """Fonction reception ser"""
        self.client.settimeout(0.5)  # timeout pour ne pas bloquer recv
        buffer = ""

        try:
            while self.connected:
                try:
                    # Lecture non bloquante (avec timeout)
                    data = self.client.recv(1024)
                    if not data:
                        # si serveur coupé ou client déconnecté
                        print("Connexion perdue (serveur fermé ?)")
                        break

                    buffer += data.decode()

                    # traiter tous les messages reçus séparés par "\n" car des fois des données peuvent être envoyé en même temps
                    while "\n" in buffer:
                        #print("in buffer")
                        line, buffer = buffer.split("\n", 1)
                        data_json = json.loads(line)

                        #print(data_json)

                        self.traiter_data(data_json)

                except socket.timeout:
                    # Pas de data → c’est normal
                    continue

                except Exception as e:
                    print(f"Erreur réception: {e}")
                    break
                
            # Sortie de boucle
            if self.connected:
                print("Serveur fermé ou erreur réseau")
                # Notifier le serveur de notre départ
                try:
                    self.client.send(json.dumps({"id": "remove client"}).encode())
                except Exception:
                    print(Exception)
            else :
                print("Déconnexion volontaire")

        finally: #Server stoppé

            self.client.close()
            self.reset_values()

    def reset_values(self):
        self.id = "Coming soon"
        self.main.state.game.player_all.dic_players.clear()
        event_queue.put({"type": "SERVER_DISCONNECTED"})

    def update_canva(self,l):
        """Envoie a C_game pour update le canva qui sera blit plus tard"""
        self.main.state.game.update_canva(l)

    def update_monster(self,l):
        """Envoie a C_game pour update les monstres qui seront blit plus tard"""
        self.main.state.game.update_monster(l)

    def traiter_data(self,data):
        """Regarde quoi faire des datas reçus + Chaque data contient un id et c'est en fonction de lui qu'on traite les données"""

        # Réception de la réponse
        id = data["id"]

        if id == "to change cell" :
            self.update_canva(data["updates"])

        elif id =="to change monster" :
            self.update_monster(data["updates"])

        elif id == "player move":
            self.main.state.game.player_all.dic_players[data["player"]].move(data["delta"])

        elif id == "set all monster" :
            #print("Init monsters")
            self.main.state.game.monsters.init_monster(data["updates"])

        elif id == "new player" :
            print(f"New connection : {data["new connection"]}")

            text = data["new connection"]
            self.id = data["new connection"]

            if data["sender"]:
                text = f"{text} (vous)"

            self.main.state.game.player_all.add_Player(self.id,
                               Img_perso = "assets/playerImg.png",
                               pos = (500,500),
                               is_you = data["sender"],
                               pseudo = text)

        elif id == "remove player":
            print(f"Remove connection : {data['remove connection']}")
            self.main.state.game.player_all.dic_players.remove(data["remove connection"])

        elif id == "start game":
            self.main.mod = "game"

        #elif id == "player move" :
            #player[data["sender"]].pos = data["pos"]

    def display_clients_name(self):
        """Affiche le nom des clients"""
        for idx,client in enumerate(self.main.state.game.player_all.dic_players.values()):
            self.draw_text(self.screen,self.font,client.pseudo,idx)

    def send_data(self,data):
        """Envoi des données au serv. json.dumps permet de convertir des dicos en texte = peut être envoyé au serv"""
        self.client.send(json.dumps(data).encode())

    def draw_text(self,screen,font,text,idx):
            text = font.render(text, True, (255, 255, 255))
            screen.blit(text, (50, 50 + idx * 30))