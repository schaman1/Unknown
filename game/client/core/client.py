import socket, select, struct, queue, threading
from shared.constants.network import PORT
from client.core.queu_event import QueueEvent
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
        self.events = QueueEvent(self.main)
        self.received_messages = queue.Queue()
        self.send_lock = threading.Lock()

        self.font = font
        self.screen = screen
        self.screen_size = self.screen.get_size()

    #def return_ip_ngrok(self,ip_port): #Pour le online
    #    """Quand on se connnecte, ecrit ip;port = ici, les séparts"""
    #    try :
    #        ipshort, port = ip_port.split(":")
    #        ip = f"{ipshort}.tcp.eu.ngrok.io"
    #        port = port
    #        print(ip,port)
    #        return ip, int(port)
#
    #    except ValueError:
    #        return None, None
        
    def connexion_serveur(self, ip="localhost"):
        "Create the client and connect to ther serveur"

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #-------- Pour ngrok = Online² --------
        #ip, port = self.return_ip_ngrok(ip_port)

        #-------- Pour local = LAN --------
        try : 
            #ip, port = ip_port.split(":")
            port = PORT
        except : 
            return self.return_err("Utilisez le format ip")
        #ip = ip.strip()
        #port = int(port) #Has to be an integer

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
        self.client.setblocking(True)
        self.received_messages = queue.Queue()
        threading.Thread(target=self._reader_loop, daemon=True).start()
        self.send_data(id = 1) #3 = client connection

    def _read_exact(self, length):
        data = bytearray()
        while len(data) < length:
            chunk = self.client.recv(length - len(data))
            if not chunk:
                raise ConnectionError("Socket closed by server")
            data.extend(chunk)
        return data

    def _reader_loop(self):
        try:
            while self.connected:
                # Read 1 byte for message ID
                msg_id_data = self._read_exact(1)
                msg_id = msg_id_data[0]
                
                # Determine message size (handling dynamic or fixed sizes)
                if msg_id in (0, 9, 19, 21, 22, 25):
                    msg_size = 1
                elif msg_id == 1:
                    msg_size = 1 + 2
                elif msg_id == 2:
                    msg_size = 1 + 1
                elif msg_id == 4:
                    count_data = self._read_exact(2)
                    count = struct.unpack("!H", count_data)[0]
                    body_len = count * 16
                    body_data = self._read_exact(body_len)
                    msg = bytearray([msg_id]) + count_data + body_data
                    self.received_messages.put(msg)
                    continue
                elif msg_id == 5:
                    count_data = self._read_exact(2)
                    count = struct.unpack("!H", count_data)[0]
                    body_len = count * 16
                    body_data = self._read_exact(body_len)
                    msg = bytearray([msg_id]) + count_data + body_data
                    self.received_messages.put(msg)
                    continue
                elif msg_id == 6:
                    msg_size = 1 + 9
                elif msg_id == 7:
                    count_data = self._read_exact(2)
                    count = struct.unpack("!H", count_data)[0]
                    body_len = count * 18
                    body_data = self._read_exact(body_len)
                    msg = bytearray([msg_id]) + count_data + body_data
                    self.received_messages.put(msg)
                    continue
                elif msg_id == 8:
                    count_data = self._read_exact(2)
                    count = struct.unpack("!H", count_data)[0]
                    body_len = count * 12
                    body_data = self._read_exact(body_len)
                    msg = bytearray([msg_id]) + count_data + body_data
                    self.received_messages.put(msg)
                    continue
                elif msg_id == 10:
                    count_data = self._read_exact(1)
                    count = struct.unpack("!B", count_data)[0]
                    body_len = 2 + count
                    body_data = self._read_exact(body_len)
                    msg = bytearray([msg_id]) + count_data + body_data
                    self.received_messages.put(msg)
                    continue
                elif msg_id == 11:
                    msg_size = 1 + 3
                elif msg_id == 12:
                    msg_size = 1 + 5
                elif msg_id == 13:
                    msg_size = 1 + 2
                elif msg_id == 14:
                    count_data = self._read_exact(2)
                    count = struct.unpack("!H", count_data)[0]
                    body_len = count * 6
                    body_data = self._read_exact(body_len)
                    msg = bytearray([msg_id]) + count_data + body_data
                    self.received_messages.put(msg)
                    continue
                elif msg_id == 15:
                    msg_size = 1 + 15
                elif msg_id == 16:
                    msg_size = 1 + 3
                elif msg_id == 17:
                    msg_size = 1 + 3
                elif msg_id == 18:
                    count_data = self._read_exact(2)
                    count = struct.unpack("!H", count_data)[0]
                    body_len = count * 6
                    body_data = self._read_exact(body_len)
                    msg = bytearray([msg_id]) + count_data + body_data
                    self.received_messages.put(msg)
                    continue
                elif msg_id == 20:
                    count_data = self._read_exact(2)
                    count = struct.unpack("!H", count_data)[0]
                    body_len = count * 6
                    body_data = self._read_exact(body_len)
                    msg = bytearray([msg_id]) + count_data + body_data
                    self.received_messages.put(msg)
                    continue
                elif msg_id == 23:
                    msg_size = 1 + 1
                elif msg_id == 24:
                    msg_size = 1 + 1
                elif msg_id == 26:
                    count_data = self._read_exact(2)
                    count = struct.unpack("!H", count_data)[0]
                    body_len = count * 4
                    body_data = self._read_exact(body_len)
                    msg = bytearray([msg_id]) + count_data + body_data
                    self.received_messages.put(msg)
                    continue
                elif msg_id == 27:
                    msg_size = 1 + 4
                elif msg_id == 28:
                    msg_size = 1 + 1
                else:
                    raise ConnectionError(f"Unknown message ID: {msg_id}")

                # Read body for static sizes
                body_data = self._read_exact(msg_size - 1)
                msg = bytearray([msg_id]) + body_data
                self.received_messages.put(msg)
        except Exception as e:
            print("Client reader thread error/disconnect:", e)
            self.received_messages.put(("disconnect", e))

    def poll_reception(self):
        while not self.received_messages.empty():
            try:
                msg = self.received_messages.get_nowait()
            except queue.Empty:
                break

            if isinstance(msg, tuple) and msg[0] == "disconnect":
                print("Connexion perdue (via queue)")
                self.connected = False
                return

            try:
                self.traiter_data(msg, len(msg))
            except Exception as e:
                print(f"Erreur lors du traitement du message {msg[0]}: {e}")
                break

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

        if id == 0:
            self.main.launch_game()

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
            id_remove = struct.unpack("!B",data[1:2])[0]
            #print("id = 2 and values = ",id_remove)
            #print(f"Remove connection : {data[1]}") #4
            #print(self.main.state.game.player_all.dic_players) #Has player 1 & 2
            self.main.state.game.player_all.dic_players.pop(id_remove, None)


        elif id == 4 : #monsters update
            self.update_monster(
                struct.unpack("!HLLLBB", data[3+i*16 : 19+i*16])
                for i in range((size-3)//16)
            )

        elif id == 5 :#Init monsters
            cells = []
            for i in range((size-3)//16):
                cells.append(struct.unpack("!HLLLBB", data[3+i*16 : 19+i*16]))

            self.main.state.game.monsters.init_monster(cells)

        elif id==6:
            id_player,pos_x,pos_y=struct.unpack("!BLL",data[1:10])
            self.events.empile((id,id_player,pos_x,pos_y))

        elif id==7: #Projectile create ?
            for i in range((size-3)//18):
                id,pos_x,pos_y,angle,vitesse,weight,id_img = struct.unpack("!LLLHHBB", data[3+i*18 : 21+i*18])

                self.main.state.game.create_projectile(id,pos_x,pos_y,angle,vitesse,weight,id_img)

        elif id==8: #Projectile die
            for i in range((size-3)//12):
                id,pos_x,pos_y = struct.unpack("!LLL",data[3+i*12:15+i*12])
                self.main.state.game.projectiles.remove_projectile(id,pos_x,pos_y)

        elif id == 9 :
            self.main.state.stop_intro()

        elif id==10:
            idx_weapon_pos,id_weapon = struct.unpack("!BB",data[2:4])
            spells_id = []

            for i in range(size-4):

                spells_id.append(struct.unpack("!B",data[4+i:5+i])[0])

            #print(spells_id,"Spells !")

            if self.main.state.game.player_all.me:
                self.main.state.game.player_all.me.add_weapon(idx_weapon_pos,id_weapon,size-7,spells_id,self.screen_size)

            #else:
            #    self.main.state.game.player_all.dic_players[client_id].add_weapon(id_weapon)

        elif id==11: 

            delta_time,id_weapon = struct.unpack("!HB",data[1:4])
            self.main.state.game.update_next_allowed_shot(delta_time,id_weapon)

        elif id==12:
            life,max_life,id = struct.unpack("!HHB",data[1:6])

            self.main.state.game.update_life(life,("Player",id,max_life))

            #self.main.state.game.create_weapon()
        
        elif id==13 :
            money = struct.unpack("!H", data[1:3])[0]
            self.main.state.game.update_money(money)
            # self.draw_money(self.screen)
            #pass

        elif id==14:

            count = struct.unpack("!H", data[1:3])[0]
            popup_to_create = []

            for i in range(count):

                id,chunk,delta_life = struct.unpack("!HHH",data[6*i+3:6*i+9])
                
                popup_to_create.append((id,chunk,delta_life))

            self.main.state.game.add_many_popup_life(popup_to_create)

        elif id==15:

            id_obj,ele_idx,id_img,pos_x,pos_y,chunk,price = struct.unpack("!BBBLLHH",data[1:16])

            self.main.state.game.objects_manager.add_object(ele_idx,id_obj,id_img,pos_x,pos_y,chunk,price)

        elif id==16:

            chunk,id_obj = struct.unpack("!HB",data[1:4])

            self.main.state.game.objects_manager.destroy_object(chunk,id_obj)

        elif id==17:
            id_weapon,id_spell,idx_pos = struct.unpack("!BBB",data[1:4])

            if self.main.state.game.player_all.me is not None:
                self.main.state.game.player_all.me.add_spell(id_weapon,id_spell,idx_pos)

        elif id==18:

            len = struct.unpack("!H", data[1:3])[0]

            for i in range(len):

                id,chunk,duree = struct.unpack("!HHH",data[6*i+3:6*i+9])
                
                self.main.state.game.kill_ent(id,chunk,duree)

        elif id == 19:
            self.main.state.add_alert("Vous devez comprendre d'ou vous venez.")

        elif id==20:

            len = struct.unpack("!H", data[1:3])[0]
            l = []

            for i in range(len):

                chunk,new_chunk,id = struct.unpack("!HHH",data[6*i+3:6*i+9])
                l.append((chunk,new_chunk,id))
                
            self.main.state.game.monsters.change_chunk(l)

        elif id==21:
            self.main.state.add_alert("Votre sac est plein !")

        elif id==22:
            self.main.state.add_alert("Vous n'avez pas assez de nifly !")

        elif id==23:

            id_weapon = data[1]
            name = {0:"Sac",1:"J",2:"K",3:"L"}
            self.main.state.add_alert(f"Reduction du temps de l'arme : {name[id_weapon]}",color = (0,255,0)) #Maybe change to put J/K/L
            if self.main.state.game.player_all.me is not None:
                self.main.state.game.player_all.me.reduce_time(id_weapon)

        elif id==24:

            id_weapon = data[1]
            name = {0:"Sac",1:"J",2:"K",3:"L"}
            self.main.state.add_alert(f"Votre arme {name[id_weapon]} a plus de place !",color = (0,255,0))

        elif id == 25:
            self.main.state.add_alert("Vous avez gagne 50PV.",color = (0,255,0))

        elif id==26:

            len = struct.unpack("!H", data[1:3])[0]
            l = []

            for i in range(len):

                chunk,id = struct.unpack("!HH",data[4*i+3:4*i+7])
                l.append((chunk,id))
                
            self.main.state.game.monsters.destroy_monster(l)

        elif id==27:
            current_hp, max_hp = struct.unpack("!HH", data[1:5])
            self.main.state.game.update_boss_health(current_hp, max_hp)

        elif id == 28:
            id_player = data[1]
            player = self.main.state.game.player_all.dic_players.get(id_player)
            if player:
                player.set_surprise()


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
            packet+= struct.pack("!B",data[0])

        elif id==5:
            packet+=struct.pack("!BBBB",data[0][0],data[0][1],data[1][0],data[1][1])

        elif id==6:
            packet+= struct.pack("!B",data[0])

        elif id==8:
            packet+= struct.pack("!HB",data[0],data[1])

        elif id==9:
            packet+= struct.pack("!BB",data[0][0],data[0][1])

        try:
            with self.send_lock:
                self.client.sendall(packet)
        except Exception as e:
            print(f"Erreur lors de l'envoi client ({id}): {e}")
            self.connected = False
        #self.client.sendall(json.dumps(data).encode())

    def draw_text(self,screen,font,text,idx):
            text = font.render(text, True, (255, 255, 255))
            screen.blit(text, (50, 50 + idx * 30))

    def stop_connection(self):
        try:
            self.send_data(id = 2)
        except:
            pass

        self.connected = None
        try:
            self.client.close()
        except:
            pass

        self.err_message = ""

        self.buffer = bytearray()
        self.events = QueueEvent(self.main)

        self.reset_values()