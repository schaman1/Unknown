from client.domain.mob.mob import Mob

class Pnj(Mob):

    def __init__(self,pos,color_idx,id,cell_size):

        super().__init__(0,0,cell_size,(8,8),"pnj")
        self.pos_x = pos[0]
        self.pos_y = pos[1]

        self.color_idx = color_idx
        self.id = id #id = id_text

    def blit(self,screen,x,y,dt):
        
        pos_blit = self.calculate_pos_blit(x,y)

        self.animation.draw(dt,pos_blit,screen)