from shared.constants import world

class Mob:

    def __init__(self, x,y,cell_size,size):
        self.pos_x = x
        self.pos_y = y
        self.base_movement = world.RATIO
        self.is_looking = 0 #0 = right / 1 = Top / 2 left / 3 bottom
        self.between_pos_x = 0
        self.between_pos_y = 0
        self.cell_size = cell_size
        self.width,self.height = size
        self.pos_blit=0

        self.life=100
        self.max_life = 100

    def update_pos_blit(self,x,y):
        self.pos_blit = self.calculate_pos_blit(x,y)

    def calculate_pos_blit(self,x,y):
        #print(self.pos_y)
        xs = self.convert_from_base(self.pos_x*self.cell_size) - self.width//2*self.cell_size +x
        ys = self.convert_from_base((self.pos_y+1) * self.cell_size) - self.height//2*self.cell_size +y #Regle un petit soucis
        return (xs,ys)
    
    def convert_from_base(self,nbr):
        return nbr//self.base_movement
    
    def update_life(self,amount):
        self.life = amount