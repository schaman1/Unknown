import pygame
from shared.constants import world
from serv.config.add_objects_begin import OBJECTS
from serv.config.add_objects_begin_admin import OBJECTS_ADDING
pygame.init()

from client.core.main import Main

#Change values to have access to all
def change_values():

    world.SPAWN_POINT = (32400,26100)

    for e in OBJECTS_ADDING:
        OBJECTS.append(e)

# Set the title of the window
pygame.display.set_caption('Unknown')

change_values()

main = Main()
main.run() #Lance le jeu