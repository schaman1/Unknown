import pygame

pygame.mixer.init()

class Sound_effect :

    def __init__(self, soundEffect, volume = 0.3):
        self.effect = pygame.mixer.Sound(soundEffect)
        self.volume = volume
        self.nb_tracks = pygame.mixer.set_num_channels(15)
        pass
    
    def nb_tracks(self, nb_track):
        self.nb_tracks = nb_track

    def play_effect(self):
        self.effect.play()
    
    def update_volume(self, volume):
        self.volume = volume