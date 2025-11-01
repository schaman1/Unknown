import pygame

class Button:
    def __init__(self,rect,color,text,font,id,border=10):
        self.rect = rect
        self.color = color
        self.border = border
        self.text = text
        self.font = font
        self.id = id
        self.pos = self.rect.center
        self.alignement = "center"
        self.clicked = False

        self.dicRect = {self.id:{
                                "rect":rect,
                                "color":color,
                                "font":font,
                                "border":border,
                                "text":text,
                                "text_color":(0,0,0)
                                }}


    def draw(self,screen):

        for ele in self.dicRect.values():

            pygame.draw.rect(screen,ele["color"],ele["rect"],border_radius = ele["border"])
            # Centrer le texte dans le rectangle
            text = self.font.render(ele["text"],True, ele["text_color"])  # True = anti-aliasing
            text_rect = text.get_rect(**{self.alignement: getattr(ele["rect"], self.alignement)})
            screen.blit(text, text_rect)

    def create_input(self,rect,color,text):

        if rect == "RIGHT":
            rect = pygame.Rect(self.rect.left + self.rect.width/3 - self.rect.height*0.2, self.rect.top + self.rect.height*0.2, self.rect.width*2/3, self.rect.height*0.6)

        self.dicRect[self.id+"_input"] = {"rect":rect,"color":color,"font":self.font,"border":self.border,"text":text,"text_color":(255,255,255 )}
        self.alignement = "midleft"
 
    def update_text(self,id,new_text):
        if id in self.dicRect:
            self.dicRect[id]["text"] = new_text
        
        else:
            print(f"Erreur : L'ID '{id}' n'existe pas dans dicRect.")