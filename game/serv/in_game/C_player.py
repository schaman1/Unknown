import var


class Player :

    def __init__(self,pos,id,screen_size,host = False) :
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.id = id
        self.is_host = host
        self.screen_size = [None,None]
        #self.set_screen_size(screen_size)

    def set_screen_size(self,screen_size):
        self.screen_size[0] = screen_size[0]//var.CELL_SIZE + var.PADDING_CANVA
        self.screen_size[1] = screen_size[1]//var.CELL_SIZE + var.PADDING_CANVA
        
    def move(self,delta) :
        self.pos_x += delta[0]
        self.pos_y += delta[1]

        return delta