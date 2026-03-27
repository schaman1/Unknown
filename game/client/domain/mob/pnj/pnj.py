from client.domain.mob.mob import Mob
from client.ui.text import AnimatedText

class Pnj(Mob):

    def __init__(self,pos,color_idx,id,cell_size,text):

        super().__init__(0,0,cell_size,(8,8),"pnj")
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.pos_blit = (0,0)

        self.color_idx = color_idx
        self.id = id #id = id_text
        self.text = AnimatedText(text,cell_size)


    def blit(self,screen,x,y,dt):
        
        self.pos_blit = self.calculate_pos_blit(x,y)

        self.animation.draw(dt,self.pos_blit,screen)

    def blit_dialogue(self,screen,dt):
        
        self.text.draw_text(screen,dt)