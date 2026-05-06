from client.config.assets import intro_images
import pygame,time

class Intro_story:

    def __init__(self,screenSize):

        self.screen_size = screenSize
        self.blit_intro = False
        self.len_images = [2,2,2,2,2] #=> 1sec for each image
        self.nbr_images = 5
        self.current_image = 0
        self.images = []
        self.time_start_intro = None
        self.pos_blit = [0,0]
            
        self.init_images()

    def init_images(self):
        for i in range(5):
            image = pygame.image.load(intro_images[i])
            size = image.get_size()
            size_y = self.screen_size[1]
            size_x = size_y*size[0]/size[1]

            image = pygame.transform.scale(image,(size_x,size_y))
            self.images.append(image)

        size_x = self.images[0].get_size()[0]

        self.pos_blit[0] = self.screen_size[0]/2-size_x/2

    def start_intro(self):
        self.current_image=0
        self.blit_intro = True
        self.time_start_intro = time.perf_counter()
    
    def stop_intro(self):
        self.blit_intro = False

    def draw_intro(self,screen):

        if not self.blit_intro :
            return None

        if self.time_start_intro+self.len_images[self.current_image]<time.perf_counter():

            self.time_start_intro+=self.len_images[self.current_image]
            self.current_image+=1

            if self.current_image>=self.nbr_images:
                self.stop_intro()
                return False
        
        screen.blit(self.images[self.current_image],self.pos_blit)
        return True

