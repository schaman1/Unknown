import pygame
from client.C_main import Main
import var
#from D_CreateCards import load_cards

pygame.init()

# Set the title of the window
pygame.display.set_caption('P_Marko')

#Load cards :
#load_cards()

main = Main()
main.run() #Lance le jeu