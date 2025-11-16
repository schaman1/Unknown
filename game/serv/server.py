import socket, threading, json
from pyngrok import ngrok
#from serv.server_game import Server_game

class Server:
    """Class mere mais ! 1 pour tout le jeu = on partage tous la même"""
    def __init__(self, intervalle,port=5000,host='0.0.0.0'):
        self.lClient = {}
        self.host = host
        self.port = port
        self.server = None
        #self.serverUDP = None #Server qui "crie" a tout le monde le ip et port du serv
        self.is_running_menu = False
        self.is_running_game = True
        self.current_thread = None
        self.nbr_player = 0
        self.intervalle_available_server = intervalle

    def handle_client(self, client_socket):
        """Gère la réception des messages d'un client connecté. = Chaque client à sa boucle handle_client"""
        try:
            while True:
                try:
                    data_recu = client_socket.recv(1024)

                    if not data_recu:
                        print(f"Client déconnecté proprement.")
                        break

                    data = json.loads(data_recu.decode())
                    addr = self.safe_peername(client_socket)
                    print(f"Reçu de {addr} : {data}")
                    if self.is_running_menu :
                        self.in_menu(data, client_socket)
                    else :
                        self.in_game(data,client_socket)

                except json.JSONDecodeError:
                    print("Erreur JSON — données corrompues ou incomplètes.")
                    continue

                except ConnectionResetError:
                    addr = self.safe_peername(client_socket)
                    print(f"Déconnexion brutale de {addr}")
                    break

                except Exception as e:
                    addr = self.safe_peername(client_socket)
                    print(f"Erreur inattendue côté client {addr} : {e}")
                    break

        finally:
                        # Déconnexion
            is_host = self.lClient.get(client_socket, {}).get("Host", False)
            if is_host:
                print("Le host a quitté, fermeture du serveur.")
                self.stop_server()
            else : 
                self.remove_client(client_socket)

    def safe_peername(self, sock):
        """Renvoie une adresse lisible ou 'inconnue' si la socket est fermée."""
        try:
            return sock.getpeername()
        except OSError:
            return "<inconnue>"

    def remove_client(self, client_socket):
        """Nettoyage propre d’un client déconnecté."""
        if client_socket in self.lClient:
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

        if data["id"] == "new client connection":
            print("New client connection")
            for client in list(self.lClient.keys()):
                meornot = (client == sender)
                text = f"Player {self.nbr_player}"
                self.send_data({
                    "id": "new player",
                    "new connection": text,
                    "sender": meornot
                }, client)

            self.set_param_on_client_arriving(sender,{"screen_size":data["screen_size"]})

        elif data["id"] == "remove client":
            print("Remove client")
            removed_id = self.lClient[sender]["id"]
            self.remove_client(sender)

            for client in list(self.lClient.keys()):
                print("Send data")
                self.send_data({
                    "id": "remove player",
                    "remove connection": removed_id
                }, client)

        elif data["id"] == "start game":
            #Redirige vers le game, stop le loop_server_in_menu pour start celui de in_game
            print("start !")
            self.is_running_menu = False
            self.is_running_game = True
            #self.server_game.lClient = self.lClient

    def in_game(self,data,sender):
        """Traite les données sachant qu'on est en jeu = saute par ex"""
        pass

    def send_data_all(self,data : dict):
        """Permet d'envoyer data a tout les clients connecté au jeu data = dico"""
        def send_to(socket):
            try:
                #print("Send successfuly")
                self.send_data(data, socket)
            except:
                print("Erreur envoi")
                pass  # ou suppression du client mort

        for socket, _ in self.lClient.items():
            threading.Thread(target=send_to, args=(socket,), daemon=True).start()

    def send_data_update(self,data : list):
        """Permet d'envoyer data a tout les clients connecté au jeu data = dico"""
        def send_to(socket,message):
            try:
                #print("Send successfuly")
                self.send_data(message, socket)
            except:
                print("Erreur envoi")
                pass  # ou suppression du client mort

        cnt = 0

        for socket, _ in self.lClient.items():
            if len(data[cnt]) != 1:
                message = {"id":"to change","updates":data[cnt][1:]}
                cnt +=1
                threading.Thread(target=send_to, args=(socket,message), daemon=True).start()

    def send_data(self, dic : dict, client):
        """Envoie des données à un client spécifique."""
        data = json.dumps(dic)
        data += "\n"
        try:
            client.send(data.encode())
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
        #self.host = socket.gethostbyname(socket.gethostname())
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #self.serverUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.serverUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #Permet d'envoyer des message a tt le monde = BORADCAST

        self.server.bind((self.host, self.port))
        print(f"Serveur lancé — host : {self.host}, port : {self.port}")

        self.server.listen() #Ecoute si des clients veulent se connecter
        self.is_running_menu = True

        # ---- 2. Lancer ngrok automatiquement ----
        public_url = ngrok.connect(self.port,"tcp")  # pour TCP brut

        ip,port = self.transforme_ngrok_ip(public_url.public_url)
        self.send_data({"id":"ngrok info","ip":ip,"port":port},client.client)

        print("URL publique ngrok:", ip,port)

        self.current_thread = threading.Thread(target=self.loop_server_menu, daemon=True).start()

        return ip,port
        #self.broadcast_server_info(self.host,self.port,"Serveur")
        #client.connexion_serveur(ip_port =f"{ip}:{port}")


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
        self.server.settimeout(1)
        while self.is_running_menu:
            try:
                client_socket, addr = self.server.accept() #Accept les clients qui veulent rejoindres #Peut faire un system de mdp ici
            except socket.timeout:
                continue
            except OSError:
                break

            print(f"Nouvelle connexion de {addr}")
            self.set_param_on_client_connection(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def set_param_on_client_arriving(self,client_socket,data):
        """Set une fois qu'a reçu la 1er donnée du client"""
        self.lClient[client_socket]["screen_size"] = data["screen_size"]
        self.lClient[client_socket]["position"] = (500,500)

    def set_param_on_client_connection(self, client_socket):
        """client_socket = le client qui s'est connecté, ici set les valeurs par default = nom / si il est host ou pas"""
        is_host = len(self.lClient) == 0
        self.nbr_player += 1
        self.lClient[client_socket] = {"Host": is_host,
                                       "id": f"Player {self.nbr_player}", #A changer, mettre cette ligne dans set param_on_client_arriving = pour le pseudo qui sera mis dans les data que le client envoie
                                       }

        for socket,client in self.lClient.items():
            
            if socket != client_socket :
                self.send_data({
                    "id": "new player",
                    "new connection": client["id"],
                    "sender": False
                }, client_socket)