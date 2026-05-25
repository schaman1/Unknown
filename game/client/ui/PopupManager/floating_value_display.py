import time,math
from client.config.display_text import FONT,FONT_SMALL

class FloatingValueDisplay:

    def __init__(self,cell_size):

        self.font = FONT
        self.speed_up = cell_size*10//3
        self.lFloatingValue = []
        self.lFloatingValueFix = []
        self.distance_max_regroup = cell_size*2

    def add_floating_value(self,text,pos,type):

        color:int
        size:int

        fix = False

        if type=="damage":
            color = (255,0,0,0)
            size = 10

        elif type=="money":
            color = (200,200,200)
            size = 10
            fix = True

        else :
            print("Unknown type. Type :",type)
            color = (0,0,0,0)
            size=10

        popup = FloatingValue(text=text,pos=pos,color = color,font = self.font,size=size,lenght_go_up=self.speed_up,fix_on_screen=fix)

        if self.check_if_another_same_value_exist(popup,fix)==False :

            if fix :
                self.lFloatingValueFix.append(popup)
            else :
                self.lFloatingValue.append(popup)

    def check_if_another_same_value_exist(self,popup,fix):

        if fix :
            l = self.lFloatingValueFix
        else :
            l = self.lFloatingValue

        for value in l :

            if value.color == popup.color :
            
                dist = math.sqrt((value.pos[0]-popup.pos[0])**2 + (value.pos[1]-popup.pos[1])**2)

                if dist<self.distance_max_regroup and value.value_init != 0 and popup.value_init!=0:

                    value.value_init+=popup.value_init
                    value.text = value.font.render(str(value.value_init), True, value.color)
                    return True
        
        return False

    def draw_floating_values(self,screen,x,y,dt):

        for i in range(len(self.lFloatingValue)-1,-1,-1) :

            destroy = self.lFloatingValue[i].draw(screen,x,y,dt)

            if destroy :
                self.lFloatingValue.pop(i)

    def draw_floating_values_fix(self,screen,x,y,pos_player,max_blit,dt):
        for i in range(len(self.lFloatingValueFix)-1,-1,-1) :

            if self.distance(pos_player,self.lFloatingValueFix[i]) < max_blit :

                destroy = self.lFloatingValueFix[i].draw(screen,x,y,dt)

                if destroy :
                    self.lFloatingValueFix.pop(i)
    
    def distance(self,pos_player,pnj):

        dist = (pos_player[0]-pnj.pos[0])**2 + (pos_player[1]-pnj.pos[1])**2
        return math.sqrt(dist)

class FloatingValue:

    def __init__(self,text,pos,color,time_lenght=2,font = None,size = 10,lenght_go_up = 0,fix_on_screen=False):

        size = font.size(str(text))

        self.pos=[pos[0]+size[0]//2,pos[1]]
        self.fix_on_screen = fix_on_screen
        self.alpha = 255
        self.color=color
        self.time_live = time_lenght
        self.time_when_destroy = time_lenght+time.perf_counter()
        self.font = font
        self.vy = lenght_go_up
        self.value_init = text

        if self.value_init!=0 :
            self.text = font.render(str(self.value_init), True, color)
        else :
            self.text = FONT_SMALL.render("Bloque", True, color)
            self.time_when_destroy -= 1 #Dure 1 sec de moins


        self.rect = self.text.get_rect(center=self.pos)

    def draw(self,screen,x,y,dt):

        self.update_pos(dt)
        self.update_rgba(dt)

        if self.fix_on_screen :
            pos_blit = (self.pos[0],self.pos[1])

        else :
            pos_blit = (self.pos[0]+x,self.pos[1]+y)

        self.rect = self.text.get_rect(center=pos_blit)
        
        screen.blit(self.text,self.rect)

        return self.is_dead()
    
    def update_pos(self,dt):

        self.pos[1]-=dt*self.vy

    def update_rgba(self,dt):
        self.alpha -= dt*255/self.time_live

        self.text.set_alpha(self.alpha)

    def is_dead(self):
        
        if time.perf_counter()>self.time_when_destroy :
            return True
        
        return False
