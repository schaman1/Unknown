

class InputHandler:

    def __init__(self):

        self.movement = {0:False,
                         1:False,
                         2:False,
                         3:False}

    def trigger(self):

        input = []
        send_jump = False

        for idx,value in (self.movement.items()):

            if value :
                input.append(idx)

        self.reset_value()

        return input

    def reset_value(self):

        self.movement[0]=False #Reset jump

    def update_value(self,idx):

        self.movement[idx]=True

    def set_false(self,key):

        self.movement[key]=False
