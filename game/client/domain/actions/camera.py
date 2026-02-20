

class Camera:

    def __init__(self,screen_size):

        self.camera_pos = [0,0]
        self.screen_size = screen_size
        self.allowed = screen_size[1]//8

        self.update_x = False
        self.update_y = False

    def return_signe(self,e):
        if e<0:
            return -1
        else:
            return 1
    
    def return_camera_pos(self,player):

        x_player,y_player = player.pos_x,player.pos_y

        x = -x_player + self.screen_size[0]//2
        y = -y_player + self.screen_size[1]//2

        delta_x = x-self.camera_pos[0]
        s_x = self.return_signe(delta_x)

        if self.update_x :
            if delta_x*s_x < self.allowed//4 :
                self.update_x = False

            else :
                self.camera_pos[0]+= delta_x//40
        
        elif delta_x*s_x > self.allowed :
            
            self.update_x = True

            self.camera_pos[0]+= delta_x//40

        delta_y = y-self.camera_pos[1]
        s_y = self.return_signe(delta_y)

        if self.update_y :

            if delta_y*s_y < self.allowed//4 :
                self.update_y = False

            else :
                self.camera_pos[1]+=delta_y//40
            
        elif delta_y*s_y > self.allowed :

            self.update_y=True

            self.camera_pos[1]+=delta_y//40

        return self.camera_pos