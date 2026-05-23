import time

class SmoothJump:

    def __init__(self,time_can_jump=0.2):

        self.time_can_jump = time_can_jump
        self.double_jump = False
        self.has_use_double_jump = False
        self.is_falling = False
        self.start_fall = None

    def can_double_jump(self):
        if self.double_jump == True and self.has_use_double_jump == False:
            self.has_use_double_jump = True
            return True
        return False

    def can_jump(self):

        if self.is_falling==False :
            return True
        
        if self.start_fall==None:
            return False
        
        elif self.start_fall + self.time_can_jump > time.perf_counter():
            self.start_fall = None
            return True

        return False

    def trigger(self,touch_ground,vy):

        if touch_ground:

            self.is_falling=False
            self.has_use_double_jump = False
            self.start_fall=None

        elif not touch_ground and vy>0 :

            if self.is_falling==False :

                self.start_fall = time.perf_counter()
                self.is_falling=True

        else :
            self.is_falling=True