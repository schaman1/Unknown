

class InputHandler:

    def __init__(self):

        self.movement = {0:False, #z
                         1:False, #d
                         2:False, #s
                         3:False,
                         7:False} #Jump, id send

    def trigger(self):

        input = []

        for idx,value in (self.movement.items()):

            if value :
                input.append(idx)

        self.reset_value()

        return input

    def reset_value(self):

        self.movement[7]=False #Reset jump

    def update_value(self,idx):

        self.movement[idx]=True

    def set_false(self,key):

        self.movement[key]=False
