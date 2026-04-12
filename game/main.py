import pygame
pygame.init()

from client.core.main import Main


# Set the title of the window
pygame.display.set_caption('P_Marko')

main = Main()
main.run() #Lance le jeu