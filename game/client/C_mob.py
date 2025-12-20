class Mob:


    def __init__(self, x,y,cell_size,size):
        self.pos_x = x
        self.pos_y = y
        self.cell_size = cell_size
        self.width,self.height = size
        #print(size)

    def calculate_pos_blit(self,x,y):
        xs = self.pos_x * self.cell_size - self.width//2*self.cell_size +x
        ys = self.pos_y * self.cell_size - self.height*self.cell_size +y
        return (xs,ys)