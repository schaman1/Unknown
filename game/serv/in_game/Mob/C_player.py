import var
from serv.in_game.Mob.C_mob import Mob

class Player(Mob) :
    '''IL FAUT METTRE EN PLACE LA VITESSE HORIZONTALE ET L'APPLIQUER DANS LES MOUVEMENTS,
    il faut aussi rajouter les dashs (vitesse horizontale temporaire) et les sauts (vitesse verticale négative)'''

    def __init__(self,pos,id,host = False, hp = 250, damage = 25, vitesse_x=1, vitesse_y=1): 

        super().__init__(pos,hp,id)

        self.hp = hp

        self.damage_taken = damage
        self.is_host = host
        self.vitesse_max = 1*self.base_movement

        self.screen_size = [None,None]
        self.size_x = 2

    def set_screen_size(self,screen_size):
        self.screen_size[0] = screen_size[0]//var.CELL_SIZE + var.PADDING_CANVA
        self.screen_size[1] = screen_size[1]//var.CELL_SIZE + var.PADDING_CANVA


    def return_delta_vitesse(self,grid_cell,cell_dur):

        self.gravity_effect(grid_cell,cell_dur)
        #print(self.pos_x,self.pos_y)

        if self.convert_from_base(self.vitesse_x+self.pos_x)>=self.screen_global_size[0]+self.size_x or self.convert_from_base(self.vitesse_x+self.pos_x)<0:
            self.vitesse_x=0

        if self.convert_from_base(self.vitesse_y+self.pos_y)>=self.screen_global_size[1] or self.convert_from_base(self.vitesse_y+self.pos_y)<0:
            self.vitesse_y=0

        deltax = self.collision_right(grid_cell,cell_dur)

        deltay = self.collision_down(grid_cell,cell_dur)


        #print(self.pos_x,self.vitesse_x,self.convert_from_base(self.vitesse_x+self.pos_x),self.screen_global_size[0])

        return (deltax,deltay)

    def update_vitesse(self):

        if self.vitesse_x<0:
            self.vitesse_x+=self.acceleration

        elif self.vitesse_x>0:
            self.vitesse_x-=self.acceleration

    def add_vitesse_to_pos(self,delta):

        pass

        #self.pos_x+=delta[0]

        #self.pos_y+=delta[1]

    def update_pos(self,grid_cell,dur,vide,liquid):

        delta = self.return_delta_vitesse(grid_cell,dur)

        self.add_vitesse_to_pos(delta)

        self.update_vitesse()

        return delta
        
    def move_from_key(self,delta,cells_arr = None,cell_dur= None,cell_vide= None,cell_liquid= None): 
        '''déplacement en fonction des collisions, peut rajouter un paramètre vitesse plus tard'''

        if delta==0:
            self.move_up(cells_arr,cell_dur)

        elif delta==1:
            self.move_down()

        elif delta==2:
            self.move_left()

        elif delta==3:
            self.move_right()
        
        #delta_collision = self.colision(delta, cells_arr, cell_dur, cell_vide, cell_liquid)        
        #self.pos_x += delta_collision[0] 
        #self.pos_y += delta_collision[1] 
        #return delta_collision

    def move_up(self,grid_cell,cell_dur):
        #self.pos_y-=1
        if self.touch_ground(grid_cell,cell_dur):
            self.vitesse_y=-20*self.acceleration

    def move_down(self):
        #self.pos_y+=1
        if self.vitesse_y<self.vitesse_max:
            self.vitesse_y+=self.acceleration

    def move_left(self):
        #self.pos_x-=1
        if self.vitesse_x>-self.vitesse_max:
            self.vitesse_x-=self.acceleration

    def move_right(self):
        #self.pos_x+=1
        if self.vitesse_x<self.vitesse_max:
            self.vitesse_x+=self.acceleration
    
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
    
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
    
    def is_alive(self):
        return self.hp > 0