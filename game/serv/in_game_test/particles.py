import random, heapq


class Sand:

    __slots__ = ('x', 'y', 'density', 'color')

    def __init__(self,x,y,density = (1,1)):
        self.x = x
        self.y = y
        self.density = density
        self.color = (random.randint(150,200),random.randint(75,140),0)

    def can_move(self,el):
        return el is None or el.__class__.__name__ == "Water"

    def update_position(self,grid,cells_h,cells_w):

        to_add = set()

        #if self.y - 1 >= 0: #A opti
         #   to_add.add((self.x, self.y - 1))

        if self.y + 1 < cells_h and self.can_move(grid[self.y + 1][self.x]):

            # on ajoute les voisins à surveiller
            if self.y - 1 >= 0:
                to_add.add((self.x, self.y - 1))

            if self.x + self.density[0] < cells_w:
                to_add.add((self.x + self.density[0], self.y - 1))

            if self.x - self.density[0] >= 0:
                to_add.add((self.x - self.density[0], self.y - 1))

            to_add.add((self.x, self.y + 1))
            to_add.add((self.x,self.y))
            self.y += 1

            return (True,( self.x,self.y),to_add) #if moved

        else:#elif random.random() < 1:  # essaie de moins unifier le sable:

            for i in range(1,self.density[0]+1):

                if self.y + 1 < cells_h and self.x - i >= 0 and self.can_move(grid[self.y + 1][self.x - i]):
                    # on ajoute les voisins à surveiller
                    if self.y - 1 >= 0:
                        to_add.add((self.x, self.y - 1))

                    for j in range(1,self.density[0]+1):
                        if self.x + j < cells_w:
                            to_add.add((self.x + j, self.y - 1))
                        
                        to_add.add((self.x - i, self.y + 1))


                    self.x -= i
                    self.y += 1
                    
                    return (True,(self.x,self.y),to_add) #if moved

                elif self.y + 1 < cells_h and self.x + i < cells_w and self.can_move(grid[self.y + 1][self.x + i]):
                    # on ajoute les voisins à surveiller
                    if self.y - 1 >= 0:
                        to_add.add((self.x, self.y - 1))

                    for j in range(1,self.density[0]+1):
                        if self.x - j >= 0:
                            to_add.add((self.x - j, self.y - 1))
                        
                        to_add.add((self.x + j, self.y + 1))


                    self.x += i
                    self.y += 1

                    return (True,(self.x,self.y),to_add) #if moved
        
        return (False,(None,None),None) #if not moved

class Wood:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        r = random.randint(0,20)
        self.color = (88-r,41-r,random.randint(0, 20))

class Fire:

    __slots__ = ('x', 'y', 'life', 'color')  # empêche la création d'un dict par instance, 2x plus rapide

    def __init__(self,x,y,life = 255):
        self.x = x
        self.y = y
        self.life = life
        self.color = (random.randint(180,255),random.randint(0,20),0,self.life)

    def update_position(self,grid,cells_h,cells_w):

        to_add = set()
        r = random.random()
        new_life=[]
        new_temp = 0
        #self.life -= random.randint(2,10)

        for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
            if 0<= self.y+i < cells_h and 0<= self.x+j < cells_w :
                name = grid[self.y+i][self.x+j].__class__.__name__
                if name == "Wood" :
                    if random.random()<0.03:
                        grid[self.y+i][self.x+j] = Fire(self.x+j,self.y+i,255)
                        to_add.add((self.x+j,self.y+i))
                    new_life.append(2000)

                elif name == "Fire" :
                    new_life.append(grid[self.y+i][self.x+j].life)

                elif name == "Water" :
                    new_temp -=200

                elif name == "Sand" :
                    new_temp -=100

        new_temp += min(sum(heapq.nlargest(4, new_life))//4-6,255)
        self.life = new_temp
        self.color = (self.color[0],self.color[1],self.color[2],self.life)
        
        if self.life <= 20 :
            if 0 <= self.y -1:
                to_add.add((self.x,self.y-1))
            return (None,(None,None),to_add)
        
        choice = random.choice([-1,0,1])
        if r > 0.5 and 0 <= self.x+choice and self.x + choice < cells_w and grid[self.y-1][self.x+choice] is None :
            to_add.add((self.x,self.y))
            to_add.add((self.x+choice,self.y-1))
            grid[self.y-1][self.x+choice] = Fire(self.x+choice,self.y-1,255)

            #self.y -=1

            return (True,(self.x,self.y),to_add)

        to_add.add((self.x,self.y))
        return (True,(self.x,self.y),to_add) #if not moved

class Water:

    __slots__ = ('x', 'y', 'cells_w', 'cells_h','color','cur_life','base_life','move')

    def __init__(self,x,y,w,h,life=40):
        self.x = x
        self.y = y
        self.move = [False,False] #(left,right)
        self.cur_life = life
        self.base_life = life
        self.cells_w = w
        self.cells_h = h
        self.color = (random.randint(0,20),random.randint(0,20),random.randint(200,255))

    def add_neighbors(self, l, x, y):
        if x-1 >= 0 :
            l.add((x-1, y))
            if y-1 >= 0:
                l.add((x-1, y-1))
        if x +1 < self.cells_w:
            l.add((x+1, y))
            if 0 <= y-1 :
                l.add((x+1, y-1))
        if 0 <= y-1 :
            l.add((x, y-1))

    def update_position(self,grid,cells_h,cells_w):

        to_add = set()
        #for i in range(100): #Test performance
            #self.add_neighbors(to_add,self.x,self.y)
            #if grid[self.y + 1][self.x] is None:
                #
            #r = random.random()

        if self.y + 1 < self.cells_h and grid[self.y + 1][self.x] is None:

            # on ajoute les voisins à surveiller
            self.add_neighbors(to_add,self.x,self.y)

            self.y += 1
            self.cur_life = self.base_life
            to_add.add((self.x, self.y))

            return (True,( self.x,self.y),to_add) #if moved

        else:#elif random.random() < 1:  # essaie de moins unifier le sable:

                if self.y + 1 < self.cells_h and self.x - 1 >= 0 and grid[self.y + 1][self.x - 1] is None:
                    # on ajoute les voisins à surveiller
                    self.add_neighbors(to_add,self.x,self.y)

                    self.x -= 1
                    self.y += 1
                    
                    to_add.add((self.x, self.y))
                    return (True,(self.x,self.y),to_add) #if moved

                elif self.y + 1 < self.cells_h and self.x + 1 < self.cells_w and grid[self.y + 1][self.x + 1] is None:
                    # on ajoute les voisins à surveiller
                    self.add_neighbors(to_add,self.x,self.y)

                    self.x += 1
                    self.y += 1
                    to_add.add((self.x, self.y))
                    return (True,(self.x,self.y),to_add) #if moved
                
                # choisir une direction
                else :
                    if self.move[0] is False and self.move[1] is False:
                        choice = random.choice([-1,1])
                        if choice == -1:
                            self.move[0] = True
                        else:
                            self.move[1] = True

                    if self.move[0] : 
                        if self.x - 1 >= 0 and grid[self.y][self.x - 1] is None:
                            #print("move left")
                            self.add_neighbors(to_add,self.x,self.y)
                            self.x -= 1
                            self.cur_life -= 1
                            if self.cur_life <= 0 :
                                if random.random() < 0.5 :
                                    self.cur_life = self.base_life
                            if self.cur_life <= 0 :
                                self.move[0] = False
                                self.move[1] = False
                                self.cur_life = self.base_life
                                return (None,(None,None),to_add)
                            else :
                                to_add.add((self.x, self.y))
                                return (True,(self.x,self.y),to_add) #if moved
                        elif self.x +1 < self.cells_w and grid[self.y][self.x + 1] is not None :
                            return (False,(None,None),None) #if not moved
                        else :
                            self.move[0] = False
                            #if self.move[1] is None :
                            self.move[1] = True
                            to_add.add((self.x, self.y))
                            return (True,(None,None),to_add)
                            #else :
                                #return (False,(None,None),None) #if not moved
                    
                    elif self.move[1] :
                        if self.x + 1 < cells_w and grid[self.y][self.x + 1] is None:
                            self.add_neighbors(to_add,self.x,self.y)
                            self.x += 1
                            self.cur_life -= 1
                            if self.cur_life <= 0 :
                                if random.random() < 0.5 :
                                    self.cur_life = self.base_life
                            if self.cur_life <= 0 :
                                self.move[0] = False
                                self.move[1] = False
                                self.cur_life = self.base_life
                                return (None,(None,None),to_add)
                            else :
                                to_add.add((self.x, self.y))
                                return (True,(self.x,self.y),to_add) #if moved
                        elif self.x -1 >= 0 and grid[self.y][self.x - 1] is not None :
                            return (False,(None,None),None) #if not moved
                        else :
                            self.move[1] = False
                            #if self.move[0] is None :
                            self.move[0] = True
                            to_add.add((self.x, self.y))
                            return (True,(None,None),to_add)
                        #else :
                         #   return (False,(None,None),None) #if not moved
    
        return (False,(None,None),None) #if not moved