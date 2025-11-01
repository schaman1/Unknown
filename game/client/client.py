import socket, json, threading, pygame
import time
from client.events import event_queue

class Client:

    def __init__(self, font,screen,main,ip="localhost", port=5000):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.client = None
        self.connected = None
        self.main = main

        self.pseudo = "Coming soon"
        self.err_message = ""

        self.lClient_id = []
        self.dic = {}

        self.font = font
        self.screen = screen

    def return_ip(self,ip_port):
        try :
            ip, port = ip_port.split(":")
            return ip, int(port)

        except ValueError:
            return None, None
        
    def connexion_serveur(self, ip_port="localhost:5000"):
        ip, port = self.return_ip(ip_port)
        if ip is None or port is None:
            return self.return_err("Utilisez le format ip:port")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        for essais in range(3):
            try:
                print(f"Tentative de connexion {essais+1}/3...")
                self.client.connect((ip, port))
                self.connection_succes()
                return
            except Exception as e:
                print(f"Échec connexion ({e}) — nouvelle tentative…")
                time.sleep(0.2)

        self.return_err("Ip ou port incorrect")

    def return_err(self,mess):
        print(mess)
        self.err_message = mess
        self.connected = False

    def connection_succes(self):
        print("Connecté au serveur")
        self.connected = True
        threading.Thread(target=self.loop_reception_server, daemon=True).start()
        
        self.client.send(json.dumps({"id":"new client connection"}).encode())
        

        #Start loop for a data for data and client

        #self.loop_client() #Test

    #def loop_client(self):

        # Envoi d'un message
        #while True:
            #pass
            #self.dic["pseudo"] = input("Ton pseudo: ")
            #self.dic["force"] = int(input("ta force"))

            #self.client.send(json.dumps(self.dic).encode())
            #print("Message envoyé")

        # Fermer la connexion
        #print("Deco")
        #self.client.close()

    def loop_reception_server(self):
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

                    # traiter tous les messages reçus séparés par "\n"
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        data_json = json.loads(line)
                        #print(f"Data reçue : {data_json}")
                        #print("2")
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
            else:
                print("Déconnexion volontaire")

            # Notifier le serveur de notre départ
            try:
                self.client.send(json.dumps({"id": "remove client"}).encode())
            except Exception:
                print(Exception)

            self.client.close()

        finally:
            self.connected = False
            self.lClient_id.clear()
            event_queue.put({"type": "SERVER_DISCONNECTED"})

    def update_canva(self,l):
        self.main.state.game.update_canva(l)

    def traiter_data(self,data):
                
        # Réception de la réponse
        id = data["id"]

        if id == "to change" :
            self.update_canva(data["updates"])
            #print("ok")

        elif id == "new player" :
            print(f"New connection : {data["new connection"]}")
            text = data["new connection"]

            if data["sender"]:
                self.pseudo = text
                text = f"{text} (vous)"
            self.lClient_id.append(text)

        elif id == "remove player":
            print(f"Remove connection : {data['remove connection']}")
            self.lClient_id.remove(data["remove connection"])

        elif id == "start game":
            self.main.mod = "game"

    def display_clients_name(self):
        for idx,client in enumerate(self.lClient_id):
            self.draw_text(self.screen,self.font,client,idx)

    def send_data(self,data):
        self.client.send(json.dumps(data).encode())

    def draw_text(self,screen,font,text,idx):
            text = font.render(text, True, (255, 255, 255))
            screen.blit(text, (50, 50 + idx * 30))