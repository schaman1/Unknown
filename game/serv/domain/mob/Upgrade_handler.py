class UpgradeHandler:

    def __init__(self):
        pass

    def trigger_event_on_player(self,list_events:list,player,dt,map):
        
        #if len(list_events)!=0:
        #    print(list_events)

        for i in range(len(list_events)-1,-1,-1) :

            id = list_events[i][0]

            if id==3:
                
                res = self.trigger_dash(list_events[i],player,dt,map)

            else :
                print("Unknown id in upgrade handle. Event :",list_events[i])
                res = False

            if res==False :
                list_events.pop(i)

    def trigger_dash(self,event,player,dt,map):
                
                delta_time,time_base,distance,angle=event[1]

                dist = distance/time_base

                distance = self.return_dist_angle(dist,angle)
                #print(distance)

                if delta_time>time_base:

                    trunca_dt = time_base-(delta_time-dt)

                    player.dash(map,trunca_dt,distance)
                    return False
                
                else :
                    player.dash(map,dt,distance)
                    if angle==90:
                        player.vitesse_y = 0
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
                    

