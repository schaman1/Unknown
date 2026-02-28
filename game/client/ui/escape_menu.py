import pygame
from client.ui.button import Button
from client.config import assets


class EscapeMenu:
    def __init__(self, screen_size, font):
        self.visible = False
        self.font = font
     
        self.overlay = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.overlay.fill((10, 10, 10, 150))
   
        largeur_panneau = int(screen_size[0] * 0.4)
        hauteur_panneau = int(screen_size[1] * 0.4)
        self.panel = pygame.Surface((largeur_panneau, hauteur_panneau), pygame.SRCALPHA)
        self.panel.fill((30, 30, 30, 200))
        self.panel_rect = self.panel.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
      
        largeur_bouton = int(largeur_panneau * 0.6)
        hauteur_bouton = int(hauteur_panneau * 0.18)
        marge_y = int(hauteur_panneau * 0.15)
        centre = self.panel_rect.centerx
        haut_y = self.panel_rect.top + marge_y + hauteur_bouton // 2
        bas_y = self.panel_rect.bottom - marge_y - hauteur_bouton // 2
        settings_btn = Button((centre, haut_y), (largeur_bouton, hauteur_bouton), assets.BTN, assets.BTN_HOVER, "Settings", font, "settings")
        quit_btn = Button((centre, bas_y), (largeur_bouton, hauteur_bouton), assets.BTN, assets.BTN_HOVER, "Quit", font, "quit")
        self.buttons = [settings_btn, quit_btn]

    def toggle(self):
        self.visible = not self.visible

    def draw(self, screen, mouse_pos):
        if not self.visible:
            return
        screen.blit(self.overlay, (0, 0))
        screen.blit(self.panel, self.panel_rect)
        for btn in self.buttons:
            btn.draw(screen, mouse_pos)

    def handle_click(self, pos):
        if not self.visible:
            return None
        for btn in self.buttons:
            if btn.get_rect().collidepoint(pos):
                return btn.id
        return None