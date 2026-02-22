

class QueueEvent:

    def __init__(self,main):

        self.q = []
        self.main = main

    def empile(self,data):
        self.q.append(data)

    def depile(self):

        return self.q.pop()
    
    def is_empty(self):
        if len(self.q) == 0:
            return True
        else :
            return False
        
    def trigger(self):
        
        while not self.is_empty():

            data = self.depile()

            id = data[0]
            if id==6:

                _,id_player,pos_x,pos_y = data

                self.main.state.game.player_all.dic_players[id_player].move((pos_x,pos_y))

