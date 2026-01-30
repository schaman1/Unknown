from client.config import assets
from shared.constants import world
import pygame

class Map:

    def __init__(self,screen_size,cell_size):
        
        self.images = assets.BG_MAP_COLORED


        self.cell_size = cell_size

        self.width_chunk,self.height_chunk = self.get_size()
        print(self.width_chunk,self.height_chunk,"Width, Height client")

        self.base_movement = world.RATIO

        self.image_to_blit = []

        image = assets.BLACK_LAYER_COLORED
        image = pygame.image.load(image).convert_alpha()
        self.black_image_colored = pygame.transform.scale(image,(self.width_chunk*self.cell_size,self.height_chunk*self.cell_size))

        self.init_images(world.SPAWN_POINT)

    def get_size(self):

        size = pygame.image.load(assets.BLACK_LAYER_UNCOLORED).convert().get_size()

        return size[0]*world.SCALE_BLOC,size[1]*world.SCALE_BLOC

    def draw_map(self,x,y,pos_player,screen):

        chunk_x,delta_x,chunk_y,delta_y = self.return_chunk_from_pos(pos_player)

        for i in range(-1,2,1):

            for j in range(-1,2,1):

                if j+chunk_x<0 or i+chunk_y<0:
                    image = self.black_image_colored
                
                else :

                    try :
                        image = self.image_to_blit[i+chunk_y][j+chunk_x]

                    except :
                        image = self.black_image_colored

                x_blit,y_blit = self.calculate_pos_blit(x,y,(chunk_x+j)*self.width_chunk,(chunk_y+i)*self.height_chunk)

                #print(j+chunk_x,j,chunk_x)

                screen.blit(image,(x_blit,y_blit))

    def calculate_pos_blit(self,x,y,pos_x,pos_y):

        xs = pos_x*self.cell_size  +x
        ys = pos_y*self.cell_size  +y #Regle un petit soucis

        return (int(xs),int(ys))

    def return_chunk_from_pos(self,pos_player):

        x,y=pos_player
        
        chunk_x = x//(self.width_chunk*self.base_movement)
        chunk_y = y//(self.height_chunk*self.base_movement)  

        delta_x = (x%self.width_chunk)/self.base_movement
        delta_y = (y%self.height_chunk)/self.base_movement

        #print(chunk_y)

        return chunk_x,delta_x,chunk_y,delta_y 

    def init_images(self,pos):

        chunk_x,_,chunk_y,_ = self.return_chunk_from_pos(pos)

        for y in range(-1,2,1):

            col = []

            for x in range(-1,2,1):

                try :

                    image = self.images[y+chunk_y+1][x+chunk_x+1]
                    image = pygame.image.load(image).convert_alpha()
                    image = pygame.transform.scale(image,(self.width_chunk*self.cell_size,self.height_chunk*self.cell_size))

                except :

                    image = self.black_image_colored
                    
                col.append(image)

            self.image_to_blit.append(col)

    def update_map_load(self,pos):
        pass



