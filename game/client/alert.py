import pygame

class Alert : 
    def __init__(self,screen,text,duration=2):
        self.screen = screen
        self.Size = (self.screen.get_width(),self.screen.get_height())
        
        self.text = text
        self.font = pygame.font.SysFont(None, 48)
        self.alert_text = self.font.render(self.text,True,(255,0,0))

        self.height = self.alert_text.get_height()

        self.calcul_rect()

        self.text_rect = self.alert_text.get_rect(center = self.rect.center)

        self.start_alert(duration)

    def calcul_rect(self):

        r = self.alert_text.get_rect()
        self.rect = pygame.Rect(0, 0, r.width + 20, r.height + 20)
        self.rect.centerx, self.rect.top = self.screen.get_width() // 2, 20

    def update_pos(self,i):
        """Update la pos de l'alert"""
        self.rect.top = (self.height+40)*i + 20
        self.text_rect = self.alert_text.get_rect(center = self.rect.center)

    def draw(self):
        """Draw the alert message on top of the screen."""

        pygame.draw.rect(self.screen,(20,20,20),self.rect,border_radius = 20)

        self.screen.blit(self.alert_text, self.text_rect)

    def start_alert(self,duration=2):
        """Display the alert for a certain duration."""
        self.start_time = pygame.time.get_ticks() + duration*1000