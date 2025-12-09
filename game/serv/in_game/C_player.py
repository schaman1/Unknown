import var


class Player :
    '''IL FAUT METTRE EN PLACE LA VITESSE HORIZONTALE ET L'APPLIQUER DANS LES MOUVEMENTS,
    il faut aussi rajouter les dashs (vitesse horizontale temporaire) et les sauts (vitesse verticale négative)'''

    def __init__(self,pos,id,screen_size,host = False, hp = 250, damage = 25, vitesse_x=1, vitesse_y=1): 
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.hp = hp

        # Vitesse de déplacement
        self.vitesse_x = vitesse_x #bassée à 1 pour les cellules
        #self.vitesse_y = vitesse_y

        self.damage_taken = damage
        self.id = id
        self.is_host = host
        self.screen_size = [None,None]
        self.set_screen_size(screen_size)

    def set_screen_size(self,screen_size):
        self.screen_size[0] = screen_size[0]//var.CELL_SIZE + var.PADDING_CANVA
        self.screen_size[1] = screen_size[1]//var.CELL_SIZE + var.PADDING_CANVA
        
    def move(self,delta,cells_arr = None,cell_dur= None,cell_vide= None,cell_liquid= None): 
        '''déplacement en fonction des collisions, peut rajouter un paramètre vitesse plus tard'''
        
        delta_collision = self.colision(delta, cells_arr, cell_dur, cell_vide, cell_liquid)        
        self.pos_x += delta_collision[0] 
        self.pos_y += delta_collision[1] 
        return delta_collision
    

    def gravite(self, vitesse_y, cells_arr,cell_dur,cell_vide,cell_liquid):
        '''Gravité simple'''
        self.vitesse_y = vitesse_y

        if self.is_type(cells_arr[self.pos_x, self.pos_y +1], cell_dur):
            pass #si cellule dur, vitesse_base reste la même

        elif self.is_type(cells_arr[self.pos_x,self.pos_y +1],cell_vide) and self.vitesse_y<4:
            self.vitesse_y*=1,5  #si cellule vide vitess_y augmente (capée à 4)

        elif self.is_type(cells_arr[self.pos_x, self.pos_y +1], cell_liquid) and self.vitesse_y<-4:
            self.vitesse_y-=0,5 #si liquide vitesse_y diminue petit à petit jusqu'à -vitesse_y pour remontée petit à petit

          

    def colision(self, delta, cells_arr,cell_dur,cell_vide,cell_liquid):
        '''Gère les collisions eau/solide avec le décor'''

        if self.is_type(cells_arr[self.pos_x +delta[0],self.pos_y],cell_dur):
            delta[0]=0  # collision avec mur, pas de déplacement

        elif self.is_type(cells_arr[self.pos_x,self.pos_y],cell_liquid):
            delta[1]=1  # collision avec eau, on déplace pos_y au niveau de l'eau

        elif self.is_type(cells_arr[self.pos_x,self.pos_y],cell_vide):
            delta[0]=1
        
        return delta


    def is_type(self, type_cell, type_check):
        """Vérifie si la cellule à la position (x,y) est du type spécifié"""
        if type_check[0] <= type_cell <= type_check[1]:
            return True
        return False
    
    
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
    
    def is_alive(self):
        return self.hp > 0
    

        