import pygame
from client.ui.button import Button
from client.config import assets


class EscapeMenu:
    def __init__(self, screen_size, font):
        self.visible = False
        self.font = font
     
        self.overlay = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.overlay.fill((10, 10, 10, 150))
   
        largeur_bouton = int(screen_size[0] * 0.25)
        hauteur_bouton = int(largeur_bouton * 0.4)
    
        centre_x = screen_size[0]//2
        centre_y = screen_size[1]//2
        setting_y = centre_y -125
        quit_y = centre_y +125
        settings_btn = Button((centre_x, setting_y), (largeur_bouton, hauteur_bouton), assets.BTN, assets.BTN_HOVER, "Settings", font, "settings")
        quit_btn = Button((centre_x, quit_y), (largeur_bouton, hauteur_bouton), assets.BTN, assets.BTN_HOVER, "Quit", font, "quit")
        self.buttons = [settings_btn, quit_btn]

    def toggle(self):
        self.visible = not self.visible

    def draw(self, screen, mouse_pos):
        if not self.visible:
            return
        screen.blit(self.overlay, (0, 0))
        for btn in self.buttons:
            btn.draw(screen, mouse_pos)

    def handle_click(self, pos):
        if not self.visible:
            return None
        for btn in self.buttons:
            if btn.get_rect().collidepoint(pos):
                return btn.id
        return None

class SettingsMenu:
    def __init__(self, screen_size, font):
        self.visible = False
        self.font = font

        self.overlay = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.overlay.fill((10, 10, 10, 200))

        self.waiting_key = None

        self.controls = {
            "inventory": pygame.K_i,
            "spell1": pygame.K_j,
            "spell2": pygame.K_k,
            "spell3": pygame.K_l,
            "right": pygame.K_d,
            "up": pygame.K_z,
            "down": pygame.K_s,
            "left": pygame.K_q,
            "jump": pygame.K_SPACE,
        }

        self.buttons = []

        centre_x = screen_size[0] // 2
        start_y = screen_size[1] // 2 - 200
        gap = 60

        i = 0
        for action in self.controls:
            btn = Button((centre_x, start_y + i * gap),(250, 50),assets.BTN,assets.BTN_HOVER,action,font,action)
            self.buttons.append(btn)
            i += 1

    def draw(self, screen, mouse_pos):
        if not self.visible:
            return

        screen.blit(self.overlay, (0, 0))

        for btn in self.buttons:
            key_name = pygame.key.name(self.controls[btn.id])
            btn.text = f"{btn.id} : {key_name}"
            btn.draw(screen, mouse_pos)

    def handle_click(self, pos):
        if not self.visible:
            return None

        for btn in self.buttons:
            if btn.get_rect().collidepoint(pos):
                self.waiting_key = btn.id
                return "waiting"

    def handle_key(self, key):
        if self.waiting_key:
            self.controls[self.waiting_key] = key
            self.waiting_key = None