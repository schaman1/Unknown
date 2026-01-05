

class Shoot_all :

    def __init__(self):
        self.next_id = 0
        self.dic_Shoot = {}

    def generate_id(self):
        self.next_id = (self.next_id+1) % 65536 #Maximum pour uint16
        return self.next_id