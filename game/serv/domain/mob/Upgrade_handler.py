class UpgradeHandler:

    def __init__(self):
        
        self.id_event_player_do = [] #Each frame player do events base on the list of id and reset  it (ex: if 1 in dahs then remove 1 from list)

    def add_event(self,events_player,player):

        for event in events_player :

            if event[0]>=40 and event[0]<50:

                player.start_dash()

    
            self.id_event_player_do.append(event)

    def trigger_event_on_player(self,player,dt,map):
        
        #if len(list_events)!=0:
        #    print(list_events)

        for i in range(len(self.id_event_player_do)-1,-1,-1) :

            id = self.id_event_player_do[i][0]

            if id>=40 and id<50:
                
                res = self.trigger_dash(self.id_event_player_do[i],player,dt,map)

            else :
                print("Unknown id in upgrade handle. Event :",self.id_event_player_do[i])
                res = False

            if res==False :
                self.id_event_player_do.pop(i)

    def trigger_dash(self,event,player,dt,map):
                
        delta_time,time_base,distance,angle=event[1]

        dist = distance/time_base

        distance = self.return_dist_angle(dist,angle)
        #print(distance)

        if delta_time>time_base:

            trunca_dt = time_base-(delta_time-dt)

            player.dash(map,trunca_dt,distance)
            player.stop_dash()
            return False
        
        else :
            player.dash(map,dt,distance)

            #if angle==90: #Y did i do that ???
            #    player.vitesse_y = 0
            
            event[1][0]+=dt
            return True
                
    def return_dist_angle(self,dist,angle):
        """return un couple de dist a faire en fonction de l'angle choisis, x/y"""

        if angle==0:
            return (dist,0)
        
        elif angle==2*90:
            return (-dist,0)
        
        elif angle==1*90:
            return (0,-dist)
        
        else :
            return(0,dist)
                    

