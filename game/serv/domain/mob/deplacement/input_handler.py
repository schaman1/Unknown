

class InputHandler:

    def __init__(self):

        self.movement = {0:False, #z
                         1:False, #d
                         2:False, #s
                         3:False,
                         7:False} #Saut, id envoyé

    def trigger(self):

        input = []

        for idx,value in (self.movement.items()):

            if value :
                input.append(idx)

        self.reset_value()

        return input
    
    def stop_mov(self):
        self.movement[0] = False
        self.movement[1] = False
        self.movement[2] = False
        self.movement[3] = False
        self.movement[7] = False

    def reset_value(self):

        self.movement[7]=False #Réinitialise le saut

    def update_value(self,idx):

        self.movement[idx]=True

    def set_false(self,key):

        self.movement[key]=False
