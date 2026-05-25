import pygame


class AnimatedText:

    def __init__(self,text_to_blit,cell_size,speed = 0.02,color = (255,255,255),text_id = 0):

        self.text_id = text_id
        self.text_to_blit = text_to_blit
        self.lenght_all_texts = len(text_to_blit)

        self.lenght_text_blit = 0
        self.start_blit_text = 0

        self.speed = speed
        self.padding_x = 1*cell_size
        self.padding_y = self.padding_x
        self.font = pygame.font.SysFont(None, cell_size*5)
        self.text_color = color

        self.lenght_current_text = None
        self.set_lenght_text()

    def set_lenght_text(self):
        self.lenght_current_text = len(self.text_to_blit[self.text_id])

    def draw_text(self,screen,dt):

        if self.lenght_text_blit<self.lenght_current_text :
            self.start_blit_text+=dt
            self.lenght_text_blit = int(self.start_blit_text//self.speed)
        
        else :
            self.lenght_text_blit=self.lenght_current_text

        current_text = self.return_current_text()

        text = self.font.render(current_text,True, self.text_color)  # True = anti-aliasing
        pos = (self.padding_x,self.padding_y)
        screen.blit(text, pos)

    def return_current_text(self):

        text = self.text_to_blit[self.text_id][0:self.lenght_text_blit]
        return text
    
    def press_enter(self):
        """Update le texte + retourne True si fin du texte = pnj dis plus rien"""
        
        if self.lenght_text_blit>=self.lenght_current_text :

            return self.next_text()

        else :
            self.lenght_text_blit=self.lenght_current_text
            return False
    
    def next_text(self):
        
        self.text_id+=1
        self.lenght_text_blit=0
        self.start_blit_text = 0

        if self.hit_end_text():
            return True
        
        else :
            self.set_lenght_text()
            return False

    def hit_end_text(self):

        if self.text_id>= self.lenght_all_texts :

            self.reset_values()

            return True
        
        return False
    
    def reset_values(self):
        self.text_id = 0
        self.lenght_text_blit = 0
        self.start_blit_text = 0