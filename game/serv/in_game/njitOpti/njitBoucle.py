from numba import njit
import numpy as np

# ---- CONSTANTES (Numba les voit ici comme des LITERALS) ----
EMPTY = 0
FIRE  = 1
STONE = 2
GRASS  = 3
WOOD  = 4
SAND = 5
EXPLO = 6
WATER = 7

IsBurnable = (WOOD,EXPLO)

propagationWood = 98

# ---- FONCTIONS NUMBA ----

@njit
def return_column(x:int,y:int,length:int,grid_color):
    """Return colonne = column"""
    moved = [(0,0,0,0,0,0)]
    for i in range(length):
        ys = y+i
        if grid_color[ys, x, 3] != 0 :
            moved.append((x,
                        y+i,                            
                        grid_color[ys, x, 0],
                        grid_color[ys, x, 1],
                        grid_color[ys, x, 2],
                        grid_color[ys, x, 3])
                        )
    return moved

@njit
def return_x_y(visible):
    n_clients,H,W = visible.shape
    max_cell = H*W
    ys_temp = np.empty(max_cell, dtype=np.int32)
    xs_temp = np.empty(max_cell, dtype=np.int32)
    count = 0

    # Parcourir toutes les cellules
    for y in range(H):
        for x in range(W):
            for c in range(n_clients):
                if visible[c, y, x]:
                    ys_temp[count] = y
                    xs_temp[count] = x
                    count += 1
                    break  # si un client voit la cellule, on peut passer à la suivante
    
    # Redimensionner les arrays pour retourner uniquement les cellules visibles
    ys = ys_temp[:count]
    xs = xs_temp[:count]
    return ys, xs

#@njit
def return_cell_update(ToUpdate,lClient,H,W):
    visible = np.zeros((len(lClient),H,W),dtype=np.bool_)
    for i,client in enumerate(lClient) :

        xs = max(client.pos_x-client.screen_size[0]//2,0)
        xe = min(client.pos_x+client.screen_size[0]//2,W)
        ys = max(client.pos_y-client.screen_size[1]//2,0)
        ye = min(client.pos_y+client.screen_size[1]//2,H)

        visible[i,ys:ye,xs:xe] = True

    result = ToUpdate & visible

    return result


@njit
def neighborns_to_update(ToUpdate,x,y):
    ToUpdate[y-1:y+2,x-1:x+2] = True

@njit
def swap_cell(ToUpdate,temperature,grid_type,grid_color,x,y,nx,ny):
    tmp,degre = grid_type[y, x],temperature[y,x]
    grid_type[y, x] = grid_type[ny, nx]
    temperature[y,x] = temperature[ny,nx]
    grid_type[ny, nx] = tmp
    temperature[ny,nx] = degre

    neighborns_to_update(ToUpdate,x,y)
    ToUpdate[y,x] = grid_type[y,x]!=0#Dis qu'il faut plus update cette cell car elle a déjà bouge = Vide / Water
    ToUpdate[ny,nx] = True #Dis qu'il faut update cette cell car elle a reçu une nouvelle cell

    # swap couleur
    for c in range(4):
        tmpc = grid_color[y, x, c]
        grid_color[y, x, c] = grid_color[ny, nx, c]
        grid_color[ny, nx, c] = tmpc

@njit
def need_update(x:int,y:int,info):
    """Si le pixel x,y est dans le champ de vision d'un client"""

    if info[0] - info[2]//2 < x and x < info[0] + info[2]//2 :
        if info[1] - info[3]//2 < y and y < info[1] + info[3]//2 :

            return True
    return False

@njit
def create_list_update(x,y,InfoClient):
    """Itere parmis tout les clients pour savoir si le client à besoin d'avoir ce pixel à update"""
    clientToUpdate = [0]
    for idx,info in enumerate(InfoClient):
        if need_update(x,y,info):
            clientToUpdate.append(idx)
    return clientToUpdate

@njit
def set_empty(ToUpdate,nx,ny,temperature,grid_type,grid_color):
    """Set nx,ny as an EMPTY cell"""
    temperature[ny,nx] = 0
    grid_type[ny,nx] = EMPTY
    grid_color[ny,nx] = (0,0,0,0)
    ToUpdate[ny,nx] = False #Dis que doit plus l'update car est plus de l'eau = Empty


@njit
def set_fire(nx,ny,temperature,grid_type,grid_color):
    """Set nx,ny as an EMPTY cell"""
    temperature[ny,nx] = 255
    grid_type[ny,nx] = FIRE
    grid_color[ny,nx] = (np.random.randint(180,255),np.random.randint(0,20),0,255)

@njit
def set_grass(nx,ny,temperature,grid_type,grid_color):
    """Set nx,ny as an EMPTY cell"""
    temperature[ny,nx] = 255
    grid_type[ny,nx] = GRASS
    grid_color[ny,nx] = (np.random.randint(60,75),np.random.randint(100,120),np.random.randint(50,60),255)

@njit
def swap_r_or_l(r_or_l,y,x,ny,nx):
    """Swap the cell for r_or_l"""
    tmp = r_or_l[y,x]
    r_or_l[y,x] = r_or_l[ny,nx]
    r_or_l[ny,nx] = tmp

@njit
def move_down_r_l(ToUpdate,x,y,H,W,temperature,grid_type,grid_color,ISEMPTY,BECOMEEMPTY): #ASEMPTY = empty pour la cell specifique
    """Return nx,ny if can move down, or down-right or down-left else : None"""
    ny = y + 1
    if ny >= H : 
        return (False,0,0)

    # test bas, bas-gauche, bas-droite
    if grid_type[ny, x] in ISEMPTY:
        nx = x
    elif x > 0 and grid_type[ny, x - 1] == EMPTY:  #Or in ISEMPTY mais bug de Edmond
        nx = x - 1
    elif x < W - 1 and grid_type[ny, x + 1] == EMPTY: #Or in ISEMPTY mais bug de Edmond
        nx = x + 1
    else:
        return (False,0,0)

    # swap type
    if grid_type[ny,nx] in BECOMEEMPTY:
        set_empty(ToUpdate,nx,ny,temperature,grid_type,grid_color)
    return (True,nx,ny)

@njit
def move_r_or_l(ToUpdate,x,y,W,r_or_l,temperature,grid_type,grid_color,ISEMPTY,BECOMEEMPTY):
    if r_or_l[y,x] is True :
        dx = -1
    else : dx = 1

    if x < W - dx and grid_type[y, x + dx] in ISEMPTY:
        nx = x + dx
        temperature[y,x] += 4

    elif x > 0 and grid_type[y, x - dx] in ISEMPTY:
        nx = x - dx
        r_or_l[y,x] = False
        temperature[y,x] += 4

    else :
        return (False,0)
        
    if grid_type[y,nx] in BECOMEEMPTY :
        set_empty(ToUpdate,nx,y,temperature,grid_type,grid_color)

    return (True,nx)

@njit
def change_pos(ToUpdate,clientToUpdate,x,y,nx,ny,moved_cells,updated,temperature,grid_type,grid_color):
    """Change the pos of the cell with it's nx,ny"""
    #else :
    swap_cell(ToUpdate,temperature,grid_type,grid_color,x,y,nx,ny)

    # on enregistre les 2 cases modifiées
    set_move(clientToUpdate,nx,ny,updated,moved_cells,grid_color)
    set_moved_cells(clientToUpdate,x,y,moved_cells,grid_color)

@njit
def set_moved_cells(clientToUpdate,x,y,moved_cells,grid_color):
    #moved_cells[0].append([x,y,grid_color[y,x]])
    #return
    for client in clientToUpdate : #List->int
        moved_cells[client].append((x, y,
                            grid_color[y, x, 0],
                            grid_color[y, x, 1],
                            grid_color[y, x, 2],
                            grid_color[y, x, 3]))

@njit
def set_move(clientToUpdate,x,y,updated,moved_cells,grid_color):
    """Set as move and to update the cell"""
    updated[y,x] = True
    set_moved_cells(clientToUpdate,x,y,moved_cells,grid_color)

@njit
def spread_fire(x,y,H,W,temperature,grid_type,grid_color,ToUpdate,clientToUpdate,updated,moved_cells,CanSpread,propagation):
    """Spread fire to adjacente cell = du to Explosion"""
        
    for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
        dy = y + i
        dx = x + j

        if 0<= dy < H and 0<= dx < W and grid_type[dy,dx] in IsBurnable :

            typ2 = grid_type[dy,dx]
            ToUpdate[dy,dx] = True #Dis qu'il faut update cette cell car y'a du feu qui monte
            set_fire(dx,dy,temperature,grid_type,grid_color)
            set_move(clientToUpdate,dx,dy,updated,moved_cells,grid_color)

            propagation = propagation-1
            if propagation <= 0 :
                return
            
            if typ2 not in CanSpread:# or typ2 == EXPLO:
                propagation = 1
                

            spread_fire(dx,dy,H,W,temperature,grid_type,grid_color,ToUpdate,clientToUpdate,updated,moved_cells,CanSpread,propagation)

@njit
def WaterSimulation(x,y,H,W,transparenceMax,ISEMPTY,BECOMEEMPTY,ToUpdate,clientToUpdate,updated,moved_cells,temperature,grid_type,grid_color,r_or_l):

    chg,nx,ny = move_down_r_l(ToUpdate,x,y,H,W,temperature,grid_type,grid_color,ISEMPTY,BECOMEEMPTY)
    if chg is True :
        grid_color[y,x,3] = transparenceMax

    else:
        ny = y
        if grid_color[y,x,3] < 50 : #cellule meurt
            neighborns_to_update(ToUpdate,x,y)
            set_empty(ToUpdate,x,y,temperature,grid_type,grid_color)
            return

        chg,nx = move_r_or_l(ToUpdate,x,y,W,r_or_l,temperature,grid_type,grid_color,ISEMPTY,BECOMEEMPTY)
        
        if chg is False :
            if grid_color[y,x,3] < transparenceMax :
                grid_color[y,x,3] +=1

                if grid_color[y,x,3] > transparenceMax :
                    grid_color[y,x,3] = transparenceMax

                set_moved_cells(clientToUpdate,x,y,moved_cells,grid_color)

            else :
                ToUpdate[y,x] = False #Dis que doit plus l'update car arrive pas à bouger
            return
        
        else :
            grid_color[y,x,3] -=4

    #else :
    change_pos(ToUpdate,clientToUpdate,x,y,nx,ny,moved_cells,updated,temperature,grid_type,grid_color)
    swap_r_or_l(r_or_l,y,x,ny,nx)

@njit
def rem_first_element(lst):
    """Remove the first element of each sublist in lst"""
    for sublist in lst:
        if len(sublist) > 0:
            sublist.pop(0)

@njit
def move_fast(ToUpdate,visible,xs,ys,grid_type, r_or_l,grid_color, temperature):

    len_client,H, W = visible.shape

    moved_cells = []
    for i in range(len_client):
        sublist = []
        sublist.append((0,0,0,0,0,0))
        moved_cells.append(sublist)

    updated = np.zeros((H, W), dtype=np.bool)  # masque des cellules déjà modifiées


    for i in range(len(xs)):
            x = xs[i]
            y = ys[i]

            clientToUpdate = np.nonzero(visible[:,y,x])[0]

            if len(clientToUpdate) == 0 :
                continue

            if updated[y,x] : 
                continue

            typ = grid_type[y, x]

            if typ == SAND:
                #continue
                chg,nx,ny = move_down_r_l(ToUpdate,x,y,H,W,temperature,grid_type,grid_color,(EMPTY,WATER,FIRE,EXPLO),(FIRE,))
                if chg is True:
                    change_pos(ToUpdate,clientToUpdate,x,y,nx,ny,moved_cells,updated,temperature,grid_type,grid_color)
                
                else :
                    ToUpdate[y,x] = False #Dis que doit plus l'update car arrive pas à bouger

            elif typ == WATER :
                WaterSimulation(x,y,H,W,255,(FIRE,EMPTY),(FIRE,),ToUpdate,clientToUpdate,updated,moved_cells,temperature,grid_type,grid_color,r_or_l)

            elif typ == EXPLO :
                WaterSimulation(x,y,H,W,127,(EMPTY,),(),ToUpdate,clientToUpdate,updated,moved_cells,temperature,grid_type,grid_color,r_or_l)

            elif typ == FIRE :
                #continue
                new_temp = temperature[y,x]
                #new_life = np.zeros(4,dtype = np.int16)
                for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
                    dy = y + i
                    dx = x + j
                    if dy < 0 or dy >= H or dx < 0 or dx >= W :
                        new_temp -= 255 
                        continue

                    temp = temperature[dy,dx]
                    typ2 = grid_type[dy,dx]
                    #if temp < 0 :
                    new_temp += temp

                    if typ2 in IsBurnable:
                        if typ2 == WOOD :
                            seuil = propagationWood 
                        #else : seuil = propagationExplo

                        if typ2 == WOOD and np.random.randint(0,100) > seuil :

                            ToUpdate[dy,dx] = True #Dis qu'il faut update cette cell car y'a du feu qui monte
                            neighborns_to_update(ToUpdate,x,y)
                            
                            set_fire(dx,dy,temperature,grid_type,grid_color)
                            set_move(clientToUpdate,dx,dy,updated,moved_cells,grid_color)
                            #a

                        elif typ2 == EXPLO :
                            spread_fire(dx,dy,H,W,temperature,grid_type,grid_color,ToUpdate,clientToUpdate,updated,moved_cells,(EXPLO,),propagation = 9999)


                new_temp = (new_temp)//5-6
                temperature[y,x] = new_temp
                grid_color[y,x,3] = new_temp

                if temperature[y,x] < 50 :

                    set_empty(ToUpdate,x,y,temperature,grid_type,grid_color)
                    # on enregistre les cases modifiées
                    set_move(clientToUpdate,x,y,updated,moved_cells,grid_color)

                    neighborns_to_update(ToUpdate,x,y)
                    continue

                if np.random.randint(0,101) > 60:
                    choice = np.random.randint(-1, 2)
                    if 0< x + choice and x+choice < W and 0<y -1 and grid_type[y-1,x+choice] == EMPTY:
                        dy = y-1
                        dx = x + choice

                        ToUpdate[dy,dx] = True #Dis qu'il faut update cette cell car y'a du feu qui monte
                        set_fire(dx,dy,temperature,grid_type,grid_color)
                        # on enregistre les cases modifiées
                        set_move(clientToUpdate,dx,dy,updated,moved_cells,grid_color)
                    
                set_moved_cells(clientToUpdate,x,y,moved_cells,grid_color)
                
            elif typ == STONE :
                #continue
                r = np.random.randint(0,100000)

                ny = y + 1
                if ny >= H :
                    continue

                for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
                    dy = y +i
                    dx = x + j
                    if dy < 0 or dy >= H or dx < 0 or dx >= W :
                        #Stoppe la boucle
                        continue

                    elif grid_type[dy,dx] in (EMPTY,WATER):
                        if r > 99998 :
                            set_grass(x,y,temperature,grid_type,grid_color)

                        set_moved_cells(clientToUpdate,x,y,moved_cells,grid_color)

            elif typ == GRASS :
                nbrGrass = 0
                for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
                    dy = y +i
                    dx = x + j
                    r = np.random.randint(0,1000)

                    if dy < 0 or dy >= H or dx < 0 or dx >= W :
                        continue

                    elif r > 997 and grid_type[dy,dx] != GRASS:
                        for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
                            ddy = dy +i
                            ddx = dx + j
                            if grid_type[ddy,ddx] == GRASS :
                                nbrGrass +=1
                        if nbrGrass < 2 or nbrGrass == 4:

                            ToUpdate[dy,dx] = True #Dis qu'il faut update cette cell car y'a du feu qui monte
                            set_grass(dx,dy,temperature,grid_type,grid_color)
                            set_move(clientToUpdate,dx,dy,updated,moved_cells,grid_color)

            
            else :
                ToUpdate[y,x] = False #Dis que doit plus l'update car arrive pas à bouger

    rem_first_element(moved_cells)
    return moved_cells