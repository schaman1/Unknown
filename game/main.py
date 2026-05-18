import pygame
pygame.init()

from client.core.main import Main


# Set the title of the window
pygame.display.set_caption('Unknown')

main = Main()
main.run() #Lance le jeu