import pygame

class Button:
    """Est utilise pour les bouttons du menu"""
    def __init__(self,pos,size,img,img_hover,text,font,id,where_blit="center"):
        self.id = id
        self.size = size
        self.text = text
        self.font = font

        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.img,size)

        self.img_hover = pygame.image.load(img_hover).convert_alpha()
        self.img_hover = pygame.transform.scale(self.img_hover,size)

        self.lImg = [self.img,self.img_hover]
        self.alignement = "center"

        self.clicked = False
        self.hover = False

        self.text_color = (0,0,0)

        self.dicRect_input = {}

        self.set_rect(where_blit,pos)
    
    def set_rect(self,where_blit,pos):
        if where_blit=="center":
            self.rect = self.img.get_rect(center=pos)
        
        elif where_blit=="topright":
            self.rect = self.img.get_rect(topright=pos)

        else :
            print("UNKNOWN pos (try center, topright ?)")


    def change_image(self):
        self.lImg[0],self.lImg[1] = self.lImg[1],self.lImg[0]
        
    def get_rect(self):
        return self.rect

    def draw(self,screen,mouse_pos):
        """Permet de draw le boutton = doit être appele pour chaque boutton crée"""

        self.check_hover(mouse_pos)

        screen.blit(self.lImg[0],self.rect)
        text = self.font.render(self.text,True, self.text_color)  # True = anti-aliasing
        text_rect = text.get_rect(**{self.alignement: getattr(self.rect, self.alignement)})
        screen.blit(text, text_rect)

        for ele in self.dicRect_input.values():

            pygame.draw.rect(screen,ele["color"],ele["rect"],border_radius = ele["border"])
            # Centrer le texte dans le rectangle
            text = ele["font"].render(ele["text"],True, ele["text_color"])  # True = anti-aliasing
            text_rect = text.get_rect(center=ele["rect"].center)

            screen.blit(text, text_rect)

    def check_hover(self,mouse_pos):

        if self.hover != self.rect.collidepoint(mouse_pos) :
            self.change_image()
            self.hover = not self.hover

    def create_input(self,rect,color,text,border):
        """Permet de creer l'input de la zone du texte dans join"""
        if rect == "RIGHT":
            rect = pygame.Rect(self.rect.left + 3*self.rect.width/22, self.rect.top + self.rect.height/3, 8*self.rect.width/11, 2*self.rect.height/5)

        self.dicRect_input[self.id+"_input"] = {"rect":rect,"color":color,"font":self.font,"border":border,"text":text,"text_color":(255,255,255)}
        self.alignement = "midtop"
        self.text_color = (255,255,255)
 
    def update_text(self,id,new_text):
        """Change le texte affiche dans le boutton"""

        if id == self.id :
            self.text = new_text

        elif id in self.dicRect_input:
            self.dicRect_input[id]["text"] = new_text

        else :
            print(f"Erreur : L'ID '{id}' n'existe pas dans dicRect.")