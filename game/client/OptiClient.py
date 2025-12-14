#from numba import njit

import pygame.surfarray as surfarray
import struct

def update_canva_surfarray(canva, data, CELL):
    rgb = surfarray.pixels3d(canva)
    alpha = surfarray.pixels_alpha(canva)

    for x, y, r, g, b, a in struct.iter_unpack("!hhBBBB", data[3:]):
        px = x * CELL
        py = y * CELL
        rgb[px:px+CELL, py:py+CELL] = (r, g, b)
        alpha[px:px+CELL, py:py+CELL] = a

    del rgb, alpha


def update_canva_njit(canva,rect_grid,l):
    """Reçoit les données l du serveur et appelle update"""
    for e in l :
        switch_cell(canva,rect_grid,e)

#@njit
def switch_cell(canva,rect_grid,el:tuple):
    """Chaque donné contient le x/y et les couleurs = dessine sur le canva !IMPORTANT : dessine pas sur le screen"""

    x,y,r,g,b,a = el
    color = (r,g,b,a)

    #self.canva.fill((0,255,0,255), pygame.Rect(500,500,50,50))
    canva.fill(color, rect_grid[y][x])