import socket, threading, sys
from serv.core.network_handler import Network_handler
from serv.systems.map.read_map import Read_map
from serv.systems.monster.read_monster import Read_monster
from serv.domain.projectile.projectile_manager import ProjectileManager
from shared.constants import world

from serv.config import network,assets
from serv.domain.mob.player import Player
#from serv.server_game import Server_game

class Server:
    """Class mere mais ! 1 pour tout le jeu = on partage tous la même"""
    def __init__(self,port=network.PORT,host='0.0.0.0'):
        self.lClient = {}
        
        self.network_handler = Network_handler(self)
        self.map_cell = Read_map(assets.BG_CELL)
        self.map_monster = Read_monster(assets.BG_MONSTER,world.SIZE_CHUNK_MONSTER,world.RATIO,self.map_cell.dur,self.map_cell.vide,self.map_cell.liquid)
        self.projectile_manager = ProjectileManager()


        self.host = host
        self.port = port
        self.server = None
        #self.serverUDP = None #Server qui "crie" a tout le monde le ip et port du serv
        self.is_running_menu = True
        self.is_running_game = False
        self.current_thread = None
        self.nbr_player = 0
        #self.intervalle_available_server = intervalle

    def safe_peername(self, sock):
        """Renvoie une adresse lisible ou 'inconnue' si la socket est fermée."""
        try:
            return sock.getpeername()
        except OSError:
            return "<inconnue>"

    def remove_client(self, client_socket):
        """Nettoyage propre d’un client déconnecté."""
        is_host = self.lClient[client_socket].is_host
        print("Suppression d'un client")

        if is_host:
            print("Le host a quitté, fermeture du serveur.")
            self.stop_server()

        elif client_socket in self.lClient:
            print(f"Suppression du client {self.safe_peername(client_socket)}")
            try:
                client_socket.close()
            except:
                pass

            if client_socket in self.network_handler.buffers:
                del self.network_handler.buffers[client_socket]

            del self.lClient[client_socket]
        else:
            print(f"Tentative de suppression d’un client déjà supprimé.")

    def stop_server(self):
        """Arrête le serveur et déconnecte tous les clients."""
        print("Arrêt du serveur...")
        for client in list(self.lClient.keys()):
            try:
                client.close()
            except:
                pass
        self.lClient.clear()
        self.nbr_player = 0

        self.is_running_menu = False
        if self.server:
            self.server.close()
            self.server = None

        print("Serveur arrêté.")

    def start_server(self, client):
        """Lance le serveur"""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #self.serverUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.serverUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #Permet d'envoyer des message a tt le monde = BORADCAST

        self.server.bind((self.host, self.port))
        print(f"Serveur lancé — host : {self.host}, port : {self.port}")

        self.server.listen() #Ecoute si des clients veulent se connecter
        self.is_running_menu = True

        # ---- Avec ngrok : ----
        #public_url = ngrok.connect(self.port,"tcp")  # pour TCP brut

        #ip,port = self.transforme_ngrok_ip(public_url.public_url)
        #print("URL publique ngrok:", ip,port)
        #self.send_data({"id":"Server info","ip":ip,"port":port},client.client)
        #self.current_thread = threading.Thread(target=self.loop_server_menu, daemon=True).start()
        #return ip,port

        # ---- Sans ngrok : ----
        self.host = socket.gethostbyname(socket.gethostname())
        #self.send_data([2,self.host,self.port],self.client)#{"id":"Server info","ip":self.host,"port":self.port},client.client)
        self.current_thread = threading.Thread(target=self.loop_server_menu, daemon=True).start()

        return self.host,self.port


        # -------------------------


    #def broadcast_server_info(self,ip,port,server_name):
    #    """Annonce la présence du serveur sur le LAN via UDP broadcast."""
#
    #    data = json.dumps({"ip":ip,
    #                        "port":port,
    #                        "name":server_name
    #    }).encode()
#
    #    threading.Thread(target = self.loop_send_data,args = (data,), daemon = True).start()
#
    #def loop_send_data(self,data):
#
    #    while self.is_running_menu :
    #        print("Broadcast")
    #        self.serverUDP.sendto(data,('255.255.255.255', self.port))
    #        time.sleep(self.intervalle_available_server)

    def transforme_ngrok_ip(self,ngrok_url):
        """Transforme l'url ngrok en ip et port"""
        try :
            url_parts = ngrok_url.split("tcp://")[1]
            ip, port = url_parts.split(":")
            return int(ip[0]), int(port)
        except Exception as e:
            print(f"Erreur transformation ngrok url: {e}")
            return None, None

    def loop_server_menu(self):
        """Loop du serveur sachant qu'on est dans le menu = accept les demandes des clients pour venir"""
        self.server.settimeout(0.5)
        while self.is_running_menu:

            self.handle_clients()
            try:
                client_socket, addr = self.server.accept() #Accept les clients qui veulent rejoindres #Peut faire un system de mdp ici
                self.set_param_on_client_arriving(client_socket)
            except socket.timeout:
                continue
            except OSError:
                break


            print(f"Nouvelle connexion de {addr}")
            
            
            #self.set_param_on_client_connection(client_socket)
            #threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def set_param_on_client_arriving(self,client_socket):
        """Set une fois qu'a reçu la 1er donnée du client"""
        is_host = len(self.lClient) == 0
        self.nbr_player += 1
        self.lClient[client_socket] = Player(pos = world.SPAWN_POINT,id = self.nbr_player,host = is_host)
        self.network_handler.buffers[client_socket] = bytearray()

    def send_data_update(self,data,id):
        self.network_handler.send_data_update(data,id)

    def send_data(self,packet,client):
        self.network_handler.send_data(packet,client)

    def send_data_all(self,data):
        """Permet d'envoyer data a tout les clients connecté au jeu data = dico"""
        def send_to(socket):
            try:
                #print("Send successfuly")
                self.send_data(data, socket)
            except Exception as e:
                #print(data)
                print(f"Erreur envoi, {e}",file=sys.stderr)
                pass  # ou suppression du client mort

        for socket in self.lClient.keys():
            threading.Thread(target=send_to, args=(socket,), daemon=True).start()

    def handle_clients(self):
        self.network_handler.handle_clients()
