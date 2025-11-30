class Player :

    def __init__(self,x,y,id) :
        self.pos_x = x
        self.pos_y = y
        self.id = id

    def move(self,delta) :
        self.pos_x += delta[0]
        self.pos_y += delta[1]