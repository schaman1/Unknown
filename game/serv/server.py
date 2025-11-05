import socket, threading, json
from serv.server_game import Server_game

class Server:
    def __init__(self, host='0.0.0.0', port=5000):
        self.lClient = {}
        self.host = host
        self.port = port
        self.server = None
        self.is_running_menu = False
        self.is_running_game = True
        self.current_thread = None
        self.nbr_player = 0
        self.server_game = Server_game(self)

    def handle_client(self, client_socket):
        """Gère la réception des messages d'un client connecté."""
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

        if data["id"] == "new client connection":
            print("New client connection")
            for client in list(self.lClient.keys()):
                meornot = (client == sender)
                text = f"Player {self.nbr_player}"
                self.send_data(json.dumps({
                    "id": "new player",
                    "new connection": text,
                    "sender": meornot
                }), client)

        elif data["id"] == "remove client":
            print("Remove client")
            removed_id = self.lClient[sender]["id"]
            self.remove_client(sender)

            for client in list(self.lClient.keys()):
                print("Send data")
                self.send_data(json.dumps({
                    "id": "remove player",
                    "remove connection": removed_id
                }), client)

        elif data["id"] == "start game":
            #Redirige vers le game, stop le loop_server_in_menu pour start celui de in_game
            print("start !")
            self.is_running_menu = False
            self.is_running_game = True
            #self.current_thread.join()
            self.send_data_all({"id":"start game"})
            result = self.server_game.init_canva()
            if result != [] :
                self.send_data_all({"id":"to change","updates":result})
            self.current_thread = threading.Thread(target=self.server_game.loop_server_game, daemon=True).start()

    def in_game(self,data,sender):
        pass

    def send_data_all(self,data):
        message = json.dumps(data)
        def send_to(socket):
            try:
                self.send_data(message, socket)
            except:
                pass  # ou suppression du client mort

        for socket, _ in self.lClient.items():
            threading.Thread(target=send_to, args=(socket,), daemon=True).start()

    def send_data(self, data, client):
        """Envoie des données à un client spécifique."""
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
        print(self.lClient)
        print("Serveur arrêté.")

    def start_server(self, port, client):
        host = socket.gethostbyname(socket.gethostname())
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        print(f"Serveur lancé — host : {host}, port : {port}")

        self.server.listen()
        self.is_running_menu = True
        self.current_thread = threading.Thread(target=self.loop_server_menu, daemon=True).start()
        client.connexion_serveur(f"{host}:{port}")

    def loop_server_menu(self):
        self.server.settimeout(1)
        while self.is_running_menu:
            try:
                client_socket, addr = self.server.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            print(f"Nouvelle connexion de {addr}")
            self.set_param_on_client_connection(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def set_param_on_client_connection(self, client_socket):
                
        is_host = len(self.lClient) == 0
        self.nbr_player += 1
        self.lClient[client_socket] = {"Host": is_host,
                                       "id": f"Player {self.nbr_player}"}

        for socket,client in self.lClient.items():
            
            if socket != client_socket :
                self.send_data(json.dumps({
                    "id": "new player",
                    "new connection": client["id"],
                    "sender": False
                }), client_socket)