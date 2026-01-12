import select,struct, threading

class Network_handler :

    def __init__(self,server) :
        self.server = server
        self.buffers = {}

    def handle_clients(self):
        """Gère la réception des messages d'un client connecté. = Chaque client à sa boucle handle_client"""
        
        #try:
        #    buffer = bytearray()
        #    while True:

        sockets = list(self.server.lClient.keys())
              
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

                self.server.remove_client(client_socket)
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

                elif msg_id==3:
                    msg_size=1+1
                
                elif msg_id==4:
                    msg_size=1

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

        if self.server.is_running_menu:
            self.in_menu(msg, client_socket)

        elif self.server.is_running_game:
            self.in_game(msg, client_socket)

    def in_menu(self, data, sender):
        """Traite les données sachant qu'on est dans le menu"""
        id_msg = struct.unpack("!B", data[0:1])[0]

        if id_msg == 1: #New client connection

            print("New client connection")

            self.send_client_already_her(sender)
            screen_size = struct.unpack("!HH", data[1:5])

            self.set_screen_size_client(sender,screen_size)
            
            for client in list(self.server.lClient.keys()):

                meornot = (client == sender)
                packet = struct.pack("!BBB", 1, self.server.nbr_player, meornot)
                self.send_data(packet,client)

                #self.send_data({
                #    "id": "new player",
                #    "new connection": text,
                #    "sender": meornot
                #}, client)

        elif id_msg == 2:
            print("Remove client")
            removed_id = self.server.lClient[sender].id
            self.server.remove_client(sender)

            for client in list(self.server.lClient.keys()):

                packet = bytearray()
                packet+=struct.pack("!BB", 2,removed_id)
                self.send_data(packet,client)

                #self.send_data({
                #    "id": "remove player",
                #    "remove connection": removed_id
                #}, client)

    def in_game(self,data,sender):
        """Traite les données sachant qu'on est en jeu = saute par ex"""

        id_msg = struct.unpack("!B", data[0:1])[0]

        if id_msg == 3 :

            dep = struct.unpack("!B", data[1:2])[0]
            self.server.lClient[sender].move_from_key(dep,self.server.map_cell.grid_type,self.server.map_cell.dur,self.server.map_cell.vide,self.server.map_cell.liquid)

        elif id_msg == 4 :
            self.server.projectile_manager.create_shoot("pioche",0,self.server.lClient[sender].return_pos())

        else :
            print("What to do with this id send ? ",id_msg)


    def send_client_already_her(self,client):
        #self.send_data({"id":"set client already connected","clients":self.lClient})

        for player in self.server.lClient.values():

            packet = struct.pack("!BBB", 1, player.id, 0)

            self.send_data(packet,client)
                           #{
                    #"id": "new player",
                    #"new connection": player.id,
                    #"sender": False
                #}, client)

    def set_screen_size_client(self,client_socket,screen_size):
        self.server.lClient[client_socket].set_screen_size(screen_size)

    def send_data_update(self,data,id):
        """Permet d'envoyer data a tout les clients connecté au jeu data = dico"""
        #print(data)
        def send_to(socket,message):
            try:
                #print("Send successfuly")
                self.send_data(message, socket)
            except Exception as e:
                print(f"Erreur envoi bis {e}")#,file=sys.stderr)
                pass  # ou suppression du client mort

        for cnt,socket in enumerate(self.server.lClient.keys()):
            if len(data[cnt]) != 0:

                threading.Thread(target=send_to, args=(socket,[id,data[cnt]]), daemon=True).start()

    def pack_cells(self,cells,packet):

        # nombre de cellules
        packet += struct.pack("!H", len(cells))

        # données des cellules
        for (x, y, r, g, b, a) in cells:
            packet += struct.pack("!hhBBBB", x, y, r, g, b, a)

        return bytes(packet)
    
    def pack_monsters(self,monsters,packet):

        #print("Pack monsters")

        # nombre de cellules

        packet += struct.pack("!H", len(monsters))

        # données des cellules
        for (chunk, id, x, y) in monsters:
            packet += struct.pack("!HLLL", chunk, id, x, y)

        return bytes(packet)
    
    def pack_projectile_create(self,projectiles,packet):

        packet += struct.pack("!H", len(projectiles))

        for (id,pos_x,pos_y,angle,v,id_img) in projectiles :

            packet+= struct.pack("!LLLHHB",id,pos_x,pos_y,angle,v,id_img)

        return bytes(packet)
    
    def pack_projectile_die(self,projectiles,packet):

        packet += struct.pack("!H", len(projectiles))

        for id in projectiles :
            packet+= struct.pack("!L",id)

        return bytes(packet)

    def send_data(self, data, client):
        """Envoie des données à un client spécifique."""

        packet = bytearray()
        id = data[0]
        packet += struct.pack("!B", id)   # envoie l’ID du message (1 octet)

        if id == 0 or id==2 or id==9:
            pass

        elif id == 1 : 
            packet+= struct.pack("!BB",data[1],data[2])

        elif id == 3:
            self.pack_cells(data[1],packet)

        elif id == 4:
            self.pack_monsters(data[1],packet)

        elif id==5:
            self.pack_monsters(data[1],packet)
            
        elif id==6:
            packet+=struct.pack("!BLL",data[1],data[2],data[3])

        elif id==7:
            self.pack_projectile_create(data[1],packet)

        elif id==8:
            self.pack_projectile_die(data[1],packet)

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

        except Exception as e:
            print(f"Erreur envoi: {e}")
