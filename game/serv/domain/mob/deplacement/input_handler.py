

class InputHandler:

    def __init__(self):

        self.movement = []

    def trigger(self):

        input = []
        send_jump = False

        for e in (self.movement):

            if e[0]==0 and send_jump==False:#Means want to jump
                send_jump=True

                input.append(e)

            elif e[0]!=0:
                input.append(e)

        self.reset_value()

        return input

    def reset_value(self):

        self.movement.clear()

    def update_value(self,idx,time):

        self.movement.append([idx,time])
