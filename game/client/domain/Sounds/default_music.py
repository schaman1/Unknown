import pygame
from random import randint

pygame.mixer.init()


class Musique :

    def __init__(self, volume=1):
        self.volume = volume
        #self.song_queue = []

        #NE REGARDE PAS CA, TU N'AS RIEN VU TKT
        self.Lmusic_walktrought = ["assets/musiques/forge-dungeon.mp3", "assets/musiques/lunch_cave.mp3", 
                                   "assets/musiques/lunch_cave.mp3", "assets/musiques/volcanic_biome.mp3", 
                                   "assets/musiques/world_discovery.mp3", "assets/musiques/world_discovery2.mp3"]
        self.Lmusic_fight = ["assets/musiques/combat_agro.mp3", "assets/musiques/combat-bossfight.mp3", 
                             "assets/musiques/crystal_crusher.mp3", "assets/musiques/crystal_crusher2.mp3", 
                             "assets/musiques/energetic-colorfull_fight.mp3", "assets/musiques/energetic-colorfull_fight2.mp3", 
                             "assets/musiques/fight_fast.mp3", "assets/musiques/Mine_bossfight.mp3"]
        
        self.taille = (len(self.Lmusic_walktrought) - 1, len(self.Lmusic_fight) -1)


    def load_music(self, name):
        self.music = pygame.mixer.music.load(name)
        self.play_music()

    def play_music(self): #volume entre 0 et 1
        pygame.mixer.music.play(loops=0, start=0, fade_ms=15000)
        pygame.mixer.music.set_volume(self.volume)

    def unload_music(self):
        self.stop_music()
        self.music = pygame.mixer.music.unload()

    def stop_music(time = 0):
        pygame.mixer.music.fadeout(time)
        #pygame.mixer.music.stop()

    
    def pause_music():
        pygame.mixer.music.pause()

    def unpause_music():
        pygame.mixer.music.unpause()


    def update_volume(new_volume):
        '''Pour dialogues ou interactions ?'''
        pygame.mixer.music.set_volume(new_volume)

    def update_music_walktrough(self):
        i = randint(0, self.taille[0])
        self.load_music(self.Lmusic_walktrought[i])
    
    def next_music(next_music):
        pygame.mixer.music.queue(next_music)
    
