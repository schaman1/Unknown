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
        

        self.Lmusic_Tim = ["assets/musiques/Tim/crystal2VF.MP3", "assets/musiques/Tim/FiestaVF.MP3",
                           "assets/musiques/Tim/Good_1.MP3", "assets/musiques/Tim/Slow_1.MP3"]
        
        
        self.music_client = "assets/musiques/Boucle client.MP3"
        
        self.taille = (len(self.Lmusic_walktrought) - 1, len(self.Lmusic_Tim) -1)
        self.Lmusics = [self.Lmusic_walktrought, self.Lmusic_Tim]


    def load_music(self, name):
        self.music = pygame.mixer.music.load(name)
        self.play_music()

    def play_music(self): #volume entre 0 et 1
        pygame.mixer.music.play(loops=0, start=0, fade_ms=15000)
        self.update_volume(self.volume)

    def unload_music(self):
        self.stop_music()
        self.music = pygame.mixer.music.unload()

    def stop_music(self, time = 1):
        self.music = pygame.mixer.music.fadeout(time)
        #pygame.mixer.music.stop()

    
    def pause_music(self):
        self.musique = pygame.mixer.music.pause()

    def unpause_music(self):
        self.musique = pygame.mixer.music.unpause()


    def update_volume(self, new_volume):
        '''Pour dialogues ou interactions ?'''
        self.music = pygame.mixer.music.set_volume(new_volume)

    def update_music_walktrough(self):
        j = randint(0, 1)
        i = randint(0, self.taille[j]) #taille de la liste de musiques walkthrough
        self.load_music(self.Lmusics[j][i])
    
    def next_music(next_music):
        pygame.mixer.music.queue(next_music)


    def client_music(self):
        self.load_music(self.music_client)
        
    
