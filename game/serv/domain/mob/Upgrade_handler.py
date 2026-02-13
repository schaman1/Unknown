class UpgradeHandler:

    def __init__(self):
        pass

    def trigger_event_on_player(self,list_events:list,player,dt,map):
        
        if len(list_events)!=0:
            print(list_events)

        for i in range(len(list_events)-1,-1,-1) :

            id = list_events[i][0]

            if id==3:
                delta_time,time_base,distance=list_events[i][1]

                dist = distance/time_base
                print("Inside, add : ",dist*dt,"With dt = ",dt)

                if delta_time>time_base:
                    player.dash(map,dt,(dist,0))
                    list_events.pop(i)
                else :
                    player.dash(map,dt,(dist,0))
                    list_events[i][1][0]+=dt
                    #list_events[i][1][1]-=dist
                    

