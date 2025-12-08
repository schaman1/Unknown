import socket, threading, struct, select
from serv.in_game.C_read_map import Read_map
from serv.in_game.C_read_monster import Read_monster
import var #Fichier
from serv.in_game.C_player import Player
#from serv.server_game import Server_game

class Server:
    """Class mere mais ! 1 pour tout le jeu = on partage tous la même"""
    def __init__(self,port=5000,host='0.0.0.0'):
        self.lClient = {}
        self.buffers = {}

        self.map_cell = Read_map(var.BG_CELL)
        self.map_monster = Read_monster(var.BG_MONSTER,var.SIZE_CHUNK_MONSTER,self.map_cell.dur,self.map_cell.vide,self.map_cell.liquid)

        self.host = host
        self.port = port
        self.server = None
        #self.serverUDP = None #Server qui "crie" a tout le monde le ip et port du serv
        self.is_running_menu = True
        self.is_running_game = False
        self.current_thread = None
        self.nbr_player = 0
        #self.intervalle_available_server = intervalle

    def handle_clients(self):
        """Gère la réception des messages d'un client connecté. = Chaque client à sa boucle handle_client"""
        
        #try:
        #    buffer = bytearray()
        #    while True:

        sockets = list(self.lClient.keys())
              
         # Ne pas appeler select sur une liste vide
        if len(sockets) == 0:
            return
        
        # select non bloquant (timeout = 0)
        readable, _, _ = select.select(sockets, [], [], 0)

        for client_socket in readable :
            try:
                data = client_socket.recv(1024)

            except BlockingIOError as e:
                    continue
            
            except Exception as e : 
                    print("Erreur reception :",e)

            if not data:
                print(f"Client déconnecté proprement.")

                self.remove_client(client_socket)
                continue

            # ajouter les données au buffer du client
            buffer = self.buffers[client_socket]
            buffer.extend(data)

            while True:
                if len(buffer) < 1:
                    break

                msg_id = buffer[0]

                # Exemple : ID 0 = start_game (1 byte)
                if msg_id == 0: #Start game
                    msg_size = 1

                elif msg_id == 1: #
                    msg_size = 1 + 4 

                else:
                    print("UNKNOWN MSG ID", msg_id)
                    del buffer[0]
                    continue

                if len(buffer) < msg_size:
                    break  # message incomplet

                msg = buffer[:msg_size]
                del buffer[:msg_size]

                # Traitement
                self.process_message(client_socket,msg,msg_size)

    def process_message(self,client_socket,msg,msg_size):
        if self.is_running_menu:
            self.in_menu(msg, client_socket)
        elif self.is_running_game:
            self.in_game(msg, client_socket)

    def safe_peername(self, sock):
        """Renvoie une adresse lisible ou 'inconnue' si la socket est fermée."""
        try:
            return sock.getpeername()
        except OSError:
            return "<inconnue>"

    def remove_client(self, client_socket):
        """Nettoyage propre d’un client déconnecté."""
        is_host = self.lClient[client_socket].is_host

        if is_host:
            print("Le host a quitté, fermeture du serveur.")
            self.stop_server()

        elif client_socket in self.lClient:
            print(f"Suppression du client {self.safe_peername(client_socket)}")
            try:
                client_socket.close()
            except:
                pass
            del self.lClient[client_socket]
        else:
            print(f"Tentative de suppression d’un client déjà supprimé.")

    def in_menu(self, data, sender):
        """Traite les données sachant qu'on est dans le menu"""
        id_msg = struct.unpack("!B", data[0:1])[0]

        if id_msg == 1: #New client connection

            print("New client connection")

            self.send_client_already_her(sender)
            screen_size = struct.unpack("!HH", data[1:5])

            self.set_screen_size_client(sender,screen_size)
            
            for client in list(self.lClient.keys()):

                meornot = (client == sender)
                packet = struct.pack("!BBB", 1, self.nbr_player, meornot)
                self.send_data(packet,client)

                #self.send_data({
                #    "id": "new player",
                #    "new connection": text,
                #    "sender": meornot
                #}, client)

        elif id_msg == 2:
            print("Remove client")
            removed_id = self.lClient[sender].id
            self.remove_client(sender)

            for client in list(self.lClient.keys()):

                packet = bytearray()
                packet+=struct.pack("!BB", 2,removed_id)
                self.send_data(packet,client)

                #self.send_data({
                #    "id": "remove player",
                #    "remove connection": removed_id
                #}, client)

        elif id_msg == 0: #1 = start game
            #Redirige vers le game, stop le loop_server_in_menu pour start celui de in_game
            print("start !")
            self.is_running_menu = False
            self.is_running_game = True

    def in_game(self,data,sender):
        """Traite les données sachant qu'on est en jeu = saute par ex"""
        id = data["id"]

        if id == "move" :
            delta = self.lClient[sender].move(data["deplacement"])
            self.send_data_all({"id":"player move","player":self.lClient[sender].id,"delta":delta})

    def send_data_all(self,data):
        """Permet d'envoyer data a tout les clients connecté au jeu data = dico"""
        def send_to(socket):
            try:
                #print("Send successfuly")
                self.send_data(data, socket)
            except Exception as e:
                print("Erreur envoi, {e}")
                pass  # ou suppression du client mort

        for socket in self.lClient.keys():
            threading.Thread(target=send_to, args=(socket,), daemon=True).start()

    def send_data_update(self,data,id):
        """Permet d'envoyer data a tout les clients connecté au jeu data = dico"""
        #print(data)
        def send_to(socket,message):
            try:
                #print("Send successfuly")
                self.send_data(message, socket)
            except Exception as e:
                print("Erreur envoi ",e)
                pass  # ou suppression du client mort

        for cnt,socket in enumerate(self.lClient.keys()):
            if len(data[cnt]) != 0:

                threading.Thread(target=send_to, args=(socket,[id,data[cnt]]), daemon=True).start()

    def pack_cells(self,cells,packet):

        # nombre de cellules
        packet += struct.pack("!H", len(cells))

        # données des cellules
        for (x, y, r, g, b, a) in cells:
            packet += struct.pack("!HHBBBB", x, y, r, g, b, a)

        return bytes(packet)
    
    def pack_monsters(self,monsters,packet):

        # nombre de cellules
        packet += struct.pack("!H", len(monsters))

        # données des cellules
        for (chunk, id, x, y) in monsters:
            packet += struct.pack("!HLHH", chunk, id, x, y)

        return bytes(packet)

    def send_data(self, data, client):
        """Envoie des données à un client spécifique."""
        packet = bytearray()
        id = data[0]
        packet += struct.pack("!B", id)   # envoie l’ID du message (1 octet)

        if id == 0 :
            pass

        elif id == 1 : 
            packet+= struct.pack("!BB",data[1],data[2])

        elif id == 2: #rem client
            pass

        elif id == 3:
            self.pack_cells(data[1],packet)

        elif id == 4:
            self.pack_monsters(data[1],packet)

        else :
            print("Issue id not found : ",id)

        try:
            client.send(packet)
        except OSError:
            # Déconnexion
            is_host = self.lClient.get(client, {}).get("Host", False)
            if is_host:
                print("Le host a quitté, fermeture du serveur.")
                self.stop_server()

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

    def send_client_already_her(self,client):
        #self.send_data({"id":"set client already connected","clients":self.lClient})

        for player in self.lClient.values():

            packet = struct.pack("!BBB", 1, player.id, 0)

            self.send_data(packet,client)
                           #{
                    #"id": "new player",
                    #"new connection": player.id,
                    #"sender": False
                #}, client)

    def set_param_on_client_arriving(self,client_socket):
        """Set une fois qu'a reçu la 1er donnée du client"""
        is_host = len(self.lClient) == 0
        self.nbr_player += 1
        self.lClient[client_socket] = Player(pos = (200,200),id = self.nbr_player,screen_size = (None,None),host = is_host)
        self.buffers[client_socket] = bytearray()

    def set_screen_size_client(self,client_socket,screen_size):
        self.lClient[client_socket].set_screen_size(screen_size)
        
        #for socket,client in self.lClient.items():
#
        #    if socket != client_socket :
        #        self.send_data({
        #            "id": "new player",
        #            "new connection": client.id,
        #            "sender": False
        #        }, client_socket)