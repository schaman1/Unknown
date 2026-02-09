import socket, select, struct
import time

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

        self.buffer = bytearray()

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
        try : 
            ip, port = ip_port.split(":")
        except : 
            return self.return_err("Utilisez le format ip:port")
        #ip = ip.strip()
        port = int(port) #Has to be an integer

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
        self.client.setblocking(False) #Pour pas bloquer le script

        #threading.Thread(target=self.loop_reception_server, daemon=True).start() #PLus besoin car le fait dans le main

        self.send_data(id = 1) #3 = client connection

    def poll_reception(self):
        """Version non bloquante de loop_reception_server(), appelée dans la boucle de jeu."""

        # Vérifie si le socket est prêt (0 = instantané)
        readable, _, _ = select.select([self.client], [], [], 0)
        if not readable:
            return  # aucune donnée, ne bloque jamais

        try:
            data = self.client.recv(1024)

        except BlockingIOError:
            print("Erreur socket non prêt")
            return  # socket non prêt (rare si select utilisé)

        except Exception as e:
            print("Erreur réception:", e)
            self.connected = False
            return

        # Déconnexion détectée
        if not data:
            print("Connexion perdue")
            self.connected = False
            return

        # Ajoute les données au buffer
        self.buffer.extend(data)

        # ---- Traitement des messages ----
        while True:

            # Besoin d'au moins 1 byte → ID
            if len(self.buffer) < 1:
                break

            msg_id = self.buffer[0]

            if len(self.buffer)<2 and (msg_id!=0 and msg_id!=2):
                break

            elif len(self.buffer)<3 and (msg_id==3 or msg_id==4 or msg_id == 5 or msg_id==7 or msg_id==8 or msg_id==10):
                break

            # Détermine la taille du message selon l'ID
            if msg_id == 0 or msg_id == 9:          # start_game / load fini
                msg_size = 1

            elif msg_id == 1:        # new player
                msg_size = 1 + 2

            elif msg_id == 2:
                msg_size = 1

            #elif msg_id == 3:
            #    msg_size = 3 + struct.unpack("!H", self.buffer[1:3])[0]*8

            elif msg_id == 4:
                msg_size = 3+struct.unpack("!H",self.buffer[1:3])[0]*14

            elif msg_id==5:
                msg_size = 3+struct.unpack("!H",self.buffer[1:3])[0]*14

            elif msg_id==6:
                msg_size = 1+9
            
            elif msg_id==7:
                msg_size = 3+struct.unpack("!H",self.buffer[1:3])[0]*18

            elif msg_id==8:
                msg_size = 3+struct.unpack("!H",self.buffer[1:3])[0]*12

            elif msg_id==10:
                msg_size = 1+4+struct.unpack("!B",self.buffer[1:2])[0]

            elif msg_id == 11 :
                msg_size = 1+3

            elif msg_id==12:
                msg_size = 1+1

            elif msg_id == 13:
                msg_size = 1+2 #id + !H (taille attendu pour traiter le tableau)

            else:
                print("UNKNOWN MSG ID", msg_id)
                self.buffer.pop(0)
                continue

            # Attendre plus de data ?
            if len(self.buffer) < msg_size:
                break

            # Extraire le message complet
            msg = self.buffer[:msg_size]

            # Retirer du buffer
            del self.buffer[:msg_size]

            # Traiter
            self.traiter_data(msg,msg_size)

    def reset_values(self):
        self.id = "Coming soon"
        self.main.state.game.player_all.dic_players.clear()

    #def update_canva(self,l):
    #    """Envoie a C_game pour update le canva qui sera blit plus tard"""
    #    self.main.state.game.update_canva(l)

    def update_monster(self,l):
        """Envoie a C_game pour update les monstres qui seront blit plus tard"""
        self.main.state.game.update_monster(l)

    def traiter_data(self,data,size):
        """Regarde quoi faire des datas reçus + Chaque data contient un id et c'est en fonction de lui qu'on traite les données"""
        id = data[0]

        # Réception de la réponse

        #if id == 3 :
        #    #cells = struct.iter_unpack("!hhBBBB", data[3:])
#
        #        #struct.unpack("!hhBBBB", data[3+i*8 : 11+i*8])
        #        #for i in range((size-3)//8)
        #    self.update_canva(
        #        data
        #    )

        if id == 4 : #monsters update
            self.update_monster(
                struct.unpack("!HLLL", data[3+i*14 : 17+i*14])
                for i in range((size-3)//14)
            )

        elif id==7: #Projectile create ?
            for i in range((size-3)//18):
                id,pos_x,pos_y,angle,vitesse,weight,id_img = struct.unpack("!LLLHHBB", data[3+i*18 : 21+i*18])

                self.main.state.game.create_projectile(id,pos_x,pos_y,angle,vitesse,weight,id_img)

        elif id==8: #Projectile die
            for i in range((size-3)//12):
                id,pos_x,pos_y = struct.unpack("!LLL",data[3+i*12:15+i*12])
                self.main.state.game.projectiles.remove_projectile(id,pos_x,pos_y)

        elif id==11: 

            delta_time,id_weapon = struct.unpack("!HB",data[1:4])
            self.main.state.game.update_next_allowed_shot(delta_time,id_weapon)

        elif id == 5 :#Init monsters
            cells = []
            for i in range((size-3)//14):
                cells.append(struct.unpack("!HLLL", data[3+i*14 : 17+i*14]))

            self.main.state.game.monsters.init_monster(cells)

        elif id==6:
            id_player,pos_x,pos_y=struct.unpack("!BLL",data[1:10])
            self.main.state.game.player_all.dic_players[id_player].move((pos_x,pos_y))


        elif id == 1 :

            print(f"New connection : {data[1]}")

            text = f"Player {data[1]}"

            if data[2]:
                self.id = data[1]
                text = f"{text} (vous)"

            self.main.state.game.player_all.add_Player(data[1],
                               is_you = data[2],
                               pseudo = text)

        elif id == 2:
            print(f"Remove connection : {data['remove connection']}")
            self.main.state.game.player_all.dic_players.remove(data["remove connection"])

        elif id == 0:
            self.main.state.mod = "intro start"

        elif id == 9 :
            self.main.state.mod = "intro end"

        elif id==10:
            client_id,idx_weapon_pos,id_weapon = struct.unpack("!BBB",data[2:5])
            spells_id = []

            for i in range(size-5):

                spells_id.append(struct.unpack("!B",data[5+i:6+i])[0])

            #print(spells_id,"Spells !")

            if client_id==self.id :
                self.main.state.game.player_all.me.add_weapon(idx_weapon_pos,id_weapon,size-7,spells_id,self.screen_size)

            else:
                self.main.state.game.player_all.dic_players[client_id].add_weapon(id_weapon)

        elif id==12:
            life = struct.unpack("!B",data[1:2])

            self.main.state.game.player_all.me.update_life(life)

            #self.main.state.game.create_weapon()
        
        elif id==13 :
            money = struct.unpack("!H", data[1:3])[0]
            self.main.state.game.player_all.me.update_money(money)
            #pass

    def display_clients_name(self):
        """Affiche le nom des clients"""
        for idx,client in enumerate(self.main.state.game.player_all.dic_players.values()):
            self.draw_text(self.screen,self.font,client.pseudo,idx)

    def send_data(self,id = None,data = None):
        """Envoi des données au serv. json.dumps permet de convertir des dicos en texte = peut être envoyé au serv"""

        packet = bytearray()
        packet += struct.pack("!B", id)

        #if id == 1 :
            #packet += struct.pack("!HH", data[0], data[1])
            
        if id == 3 :
            packet+= struct.pack("!B",data[0])

        elif id == 4:
            packet+= struct.pack("!H",data[0])

        elif id==5:
            packet+=struct.pack("!BBBB",data[0][0],data[0][1],data[1][0],data[1][1])

        self.client.send(packet)
        #self.client.send(json.dumps(data).encode())

    def draw_text(self,screen,font,text,idx):
            text = font.render(text, True, (255, 255, 255))
            screen.blit(text, (50, 50 + idx * 30))