import pygame, time, json
from utils.resource_path import resource_path
from client.domain.mob.player.player_all import Player_all
from client.domain.mob.monster.monster_all import Monster_all
from client.domain.mob.pnj.pnj_all import Pnj_all
from client.domain.projectile.projectile_manager import ProjectileManager
from client.ui.PopupManager.floating_value_display import FloatingValueDisplay
from client.ui.objects.objects_manager import objects_manager
#from client.domain.actions.mini_map import MiniMap
from client.domain.actions.map import Map
from client.domain.actions.camera import Camera
from client.domain.intro.intro_story import Intro_story
from client.ui.add_fading import Fading
from client.ui.text import AnimatedText
from client.config import assets
from shared.constants import world
from client.config.display_text import FONT, FONT_SMALL

class Game :
    """Class utilise quand lance le jeu / Permet d'afficher le jeu en gros et devra mettre plus tard les persos à afficher"""
    def __init__(self, cell_size, screenSize):
        self.canva_size = world.BG_SIZE_SERVER
        self.base_movement = world.RATIO
        self.end = False
        self.end_alpha_len = 6
        self.end_img = pygame.image.load(assets.BG_END).convert()
        size = self.end_img.get_size()
        scale = (screenSize[0])*size[1]//size[0]
        self.end_img = pygame.transform.scale(self.end_img,(screenSize[0],scale))
        self.last_time_add_text_end = time.perf_counter()
        self.nbr_text_end = 0
        self.end_text = []
        with open(resource_path("client/ui/json/text.json")) as f:

            dialogues = json.load(f)
            f.close()
        self.text_to_blit_end = dialogues["End"]

        self.cell_size = cell_size
        self.screen_size = screenSize
        self.center = (screenSize[0]//2,screenSize[1]//2)
        
        #self.canva = pygame.Surface((self.canva_size[0]*cell_size,self.canva_size[1]*cell_size), pygame.SRCALPHA)
        self.canva = Map(screenSize,cell_size)
        self.len_can_blit = self.screen_size[0]//2
        
        self.grey_layer = pygame.Surface(screenSize,pygame.SRCALPHA)
        self.grey_layer.fill((10,10,10,150))

        self.waiting_img = pygame.image.load(assets.BG_WAITING).convert()
        self.fading_layer = pygame.Surface(screenSize,pygame.SRCALPHA)
        self.alpha_fading = 255
        size = self.waiting_img.get_size()
        scale = (screenSize[0]//2)*size[1]//size[0]
        self.waiting_img = pygame.transform.scale(self.waiting_img,(screenSize[0]//2,scale))
        self.rect_img_waiting = self.waiting_img.get_rect(center = ((screenSize[0]//2,screenSize[1]//2)))

        self.team_img = pygame.image.load(assets.TEAM_NIKA).convert()
        size = self.team_img.get_size()
        scale = (screenSize[0]//4)*size[1]//size[0]
        self.team_img = pygame.transform.scale(self.team_img,(screenSize[0]//4,scale))
        self.rect_img_team = self.team_img.get_rect(center = ((screenSize[0]//2,screenSize[1]*3//4)))
        
        #For fading on intro
        self.len_fading = 2
        self.end_fading = None

        #self.bg = pygame.image.load(assets.BG_GLOBAL).convert()
        #self.bg = pygame.transform.scale(self.bg, (self.canva_size[0],self.canva_size[1]))

        self.monsters = Monster_all(cell_size)

        self.player_all = Player_all(cell_size,screenSize)

        self.pnj_all = Pnj_all(cell_size,screenSize)

        #self.mini_map = MiniMap(world.NBR_CELL_CAN_SEE,assets.MAP_SEEN,assets.MAP_UNSEEN,self.canva_size,self.cell_size)

        self.projectiles = ProjectileManager(cell_size)

        self.floating_values = FloatingValueDisplay(cell_size)

        self.objects_manager = objects_manager(cell_size)

        self.camera = Camera(screenSize)

        self.intro_story = Intro_story(self.screen_size)

        self.fade = Fading(screenSize)

        self.player_command = []
        self.blit_info=False
        self.spell_blit_mouse=None
        self.boss_hp = None
        self.boss_max_hp = None
        self.boss_bar_alpha = 0.0

    def draw_story(self):
        self.intro_story.start_intro()
        
    def draw_intro_start(self,screen):

        screen.blit(self.waiting_img,self.rect_img_waiting)
        screen.blit(self.team_img,self.rect_img_team)

    def draw_intro_end(self,screen,dt,mouse_pos):

        self.draw(screen,dt,mouse_pos)
        self.fading_layer.fill((0,0,0,self.alpha_fading))
        screen.blit(self.fading_layer,(0,0))

        self.waiting_img.set_alpha(self.alpha_fading)
        self.team_img.set_alpha(self.alpha_fading)

        screen.blit(self.waiting_img,self.rect_img_waiting) #Faire un decrescendo ou un truc stylé d'animation
        screen.blit(self.team_img,self.rect_img_team)

        delta_time = max(self.end_fading - time.perf_counter(),0)
        self.alpha_fading = int(255*delta_time/self.len_fading)

        if delta_time<=0 :
            return True
    
        return False #True If end animation else return False
    
    def draw_end(self,screen,dt):

        if self.alpha_fading != 255 :

            self.fading_layer.fill((0,0,0,self.alpha_fading))
            screen.blit(self.fading_layer,(0,0))

            self.end_img.set_alpha(self.alpha_fading)

            screen.blit(self.end_img,(0,0)) #Faire un decrescendo ou un truc stylé d'animation

            delta_time = max(self.end_alpha_fading - time.perf_counter(),0)
            self.alpha_fading = int(255*(1-(delta_time)/self.end_alpha_len))

        else :
            screen.blit(self.end_img,(0,0)) #Faire un decrescendo ou un truc stylé d'animation

            if self.last_time_add_text_end < time.perf_counter() and self.nbr_text_end < 11:
                self.last_time_add_text_end += 1
                text = AnimatedText(self.text_to_blit_end,self.cell_size,text_id = self.nbr_text_end)
                text.padding_y = self.screen_size[1]
                text.padding_x = self.cell_size*10
                text.lenght_text_blit = text.lenght_current_text
                self.end_text.append(text)
                self.nbr_text_end +=1

            for text in self.end_text :

                text.draw_text(screen,dt)
                text.padding_y-=dt*(self.screen_size[1]//10)

    def update_monster(self,data_monster):
        """Reçoit les données des monstres du serv et les envoie à Monster_all"""

        for (chunk, id, x, y, state,side) in data_monster :

            self.monsters.dic_monster[chunk][id].move((x,y))
                
            self.monsters.dic_monster[chunk][id].change_state(state,side)

    def shot(self,id_key):
        if not self.blit_info:
            self.player_command.append(self.player_all.me.shot(id_key))

    def blit_monsters(self,screen,x,y,pos_player,max_blit,dt):
        self.monsters.blit_all_monsters(screen,x,y,pos_player,max_blit,dt)

    def blit_players(self,screen,x,y,pos_player,max_blit,dt):
        self.player_all.blit_players(screen,x,y,pos_player,max_blit,dt)

    def blit_pnj(self,screen,x,y,pos_player,max_blit,dt):
        self.pnj_all.blit_pnj(screen,x,y,dt,pos_player,max_blit)

    def blit_projectiles_explosions(self,screen,x,y,dt):

        self.projectiles.blit_projectiles_explosions(screen,x,y,dt)

    def blit_utils(self,screen,screen_size):

        self.player_all.blit_client_utils(screen,screen_size)

    def blit_infos(self,screen,screen_size,mouse_pos):

        if self.blit_info :

            screen.blit(self.grey_layer,(0,0))

            #screen.fill((50,50,50)) #A changer pour mettre transparence

            self.player_all.blit_infos(screen,screen_size,mouse_pos)

            if self.spell_blit_mouse!=None:
                pos = [mouse_pos[0]-self.cell_size,mouse_pos[1]-self.cell_size]

                screen.blit(self.spell_blit_mouse,pos)

    def draw(self,screen,dt,mouse_pos=None):
        """Blit le canva sur le screen à la position x,y + return weither is in interaction or not"""

        #if 1/dt < 100 :
        #    print("Fps : ",1/dt)

        x,y = self.camera.return_camera_pos(self.player_all.me)
        pos_player = self.player_all.return_pos()

        #screen.blit((0,0,0))
        #screen.fill((0,0,0))

        self.canva.draw_map(x,y,self.player_all.return_pos(),screen)

        self.objects_manager.blit_all_objects(screen,x,y,pos_player,self.len_can_blit,dt)
        self.blit_pnj(screen,x,y,pos_player,self.len_can_blit,dt)
        self.blit_monsters(screen,x,y,pos_player,self.len_can_blit,dt)
        self.blit_players(screen,x,y,pos_player,self.len_can_blit,dt)

        self.blit_projectiles_explosions(screen,x,y,dt)
        self.floating_values.draw_floating_values(screen,x,y,dt)

        self.player_all.draw_light(screen,self.projectiles.projectiles_lumiere,x,y,pos_player,self.len_can_blit)

        self.floating_values.draw_floating_values_fix(screen,x,y,pos_player,self.len_can_blit,dt)

        self.blit_utils(screen,self.screen_size)

        pos = (self.convert_from_base(pos_player[0]),self.convert_from_base(pos_player[1]))

        self.pnj_all.blit_dialogue(screen,dt)
        #self.mini_map.draw_map(screen,pos)
        self.blit_infos(screen,self.screen_size,mouse_pos)

        self.draw_boss_health_bar(screen, dt)

        self.fade.trigger(screen,dt)

        in_interaction = self.intro_story.draw_intro(screen)

        if self.end:
            self.draw_end(screen,dt)

        return in_interaction

    def convert_from_base(self,nbr): #Est utilisé ???
        return nbr//self.base_movement
    
    def create_projectile(self,id,pos_x,pos_y,angle,vitesse,weight,id_img):

        self.projectiles.create_projectile(id,pos_x,pos_y,angle,vitesse,weight,id_img)

    def update_next_allowed_shot(self,delta_time,id_weapon):

        self.player_all.me.weapons.update_next_allowed_shot(delta_time,id_weapon)

    def trigger_mouse_down(self,mouse_pos):

        if self.blit_info :

            info,spell_1,spell_2 =  self.player_all.mouse_button_down(mouse_pos)

            if info==1:
                self.spell_blit_mouse = None

            elif info==0: #Blit spell_1 a pos=souris car c l'img du spell
                self.spell_blit_mouse =spell_1 

            elif info==-1 and spell_1!=None: #In air
                self.spell_blit_mouse = None


            return info,spell_1,spell_2
        
        else :

            return -1,None,None
        
    def stop_blit_info(self):
        """Stop blit info and return True if effectively stop blitting info"""

        if self.blit_info == True :
            self.blit_info = False
            if self.blit_info and self.spell_blit_mouse != None:
                
                self.player_all.me.weapons.stop_holding_spell()
                self.spell_blit_mouse=None

            return True
        return False

        
    def trigger_info_key(self):

        if self.blit_info and self.spell_blit_mouse != None:
            
            self.player_all.me.weapons.stop_holding_spell()
            self.spell_blit_mouse=None

        self.blit_info = not self.blit_info

    def update_life(self,new_life,data):
        
        id = data[0]

        if id=="Player" :

            #delta_life = new_life - self.player_all.me.life
            #self.add_popup(self.player_all.me,delta_life)

            id_player = data[1]
            max_life = data[2]

            self.player_all.dic_players[id_player].update_life(new_life,max_life)

    def update_money(self,money):

        delta_money = self.player_all.me.update_money(money)

        pos = [self.player_all.me.pos_blit_text[0],self.player_all.me.pos_blit_text[1]]

        if delta_money>0:
            delta_money_txt = "+"+str(delta_money)

        else :
            delta_money_txt = str(delta_money)

        self.add_popup_on_screen(pos,str(delta_money_txt),type = "money")
    
    def add_popup(self,ent,text,type = "damage"):

        self.floating_values.add_floating_value(text,[ent.pos_x,ent.pos_y],type)

    def add_popup_on_screen(self,pos,text,type):
        self.floating_values.add_floating_value(text,pos,type)

    def add_many_popup_life(self,data):

        for e in data:

            id,chunk,delta_life = e

            if chunk==99: #Magic number je sais mais nsm
                ent = self.player_all.dic_players[id]
                self.add_popup(ent,delta_life)
            else :
                ent = self.monsters.dic_monster[chunk].get(id)
                if ent is not None:

                    self.add_popup(ent,delta_life)

    def interact(self):
        """Look around player if can interact with an object + interact with the closest one """

        pos_player = self.player_all.return_pos()

        touch_pnj = False

        res = self.objects_manager.test_trigger(pos_player)

        if res!=None:

            touch_pnj = self.pnj_all.test_trigger(pos_player,res[0])

            if not touch_pnj and res[1]!=None:

                if res[2] == 5  and self.player_all.me.money< 1: #Element.price quoi
                    #=> dans l'intro
                    touch_pnj = self.pnj_all.test_trigger(pos_player,None) #Pour parler avec le pnj
                    return False,"Tue un monstre pour avoir assez de Nifly"

                else :
                    chunk,id = res[1]
                    self.objects_manager.chunk_objects[chunk][id].start_anim_trigger()
                    self.player_command.append([8,chunk,id])

                    if res[2]==5 :#Means take the spell begin
                        self.pnj_all.change_text_pnj("pnj_learn_attack","pnj_learn_spell")
                        touch_pnj = self.pnj_all.test_trigger(pos_player,None)

            return touch_pnj,None

        else :
        
            return False,None
        
    def kill_ent(self,id,chunk,duree):
        """Put the death animation on target ent"""

        duree = duree/1000
    
        if chunk==99 :
            self.player_all.dic_players[id].kill(duree)
            if self.player_all.dic_players[id] == self.player_all.me :
                self.fade.set_values(3,duree-3-0.2*4)

        else :
            self.monsters.dic_monster[chunk][id].kill(duree)
            if self.monsters.dic_monster[chunk][id].name == "DwarfKing" :
                self.start_end()

    def start_end(self):
        self.end = True
        self.end_alpha_fading = time.perf_counter()+self.end_alpha_len
        self.alpha_fading = 0
        self.last_time_add_text_end = time.perf_counter()+self.end_alpha_len

    def update_boss_health(self, current_hp, max_hp):
        self.boss_hp = current_hp
        self.boss_max_hp = max_hp

    def draw_boss_health_bar(self, screen, dt):
        in_boss_zone = False
        if hasattr(self, 'canva') and self.canva.chunk_x is not None and self.canva.chunk_y is not None:
            # Chunks for x11y7 - x12y7: chunk_y == 7, chunk_x in (11, 12)
            in_boss_zone = (self.canva.chunk_y == 7 and self.canva.chunk_x in (11, 12))

        fade_duration = 1.0
        alpha_change = (255.0 * dt) / fade_duration
        
        boss_alive = self.boss_hp is not None and self.boss_hp > 0
        
        if in_boss_zone and boss_alive:
            self.boss_bar_alpha = min(255.0, self.boss_bar_alpha + alpha_change)
        else:
            self.boss_bar_alpha = max(0.0, self.boss_bar_alpha - alpha_change)

        if self.boss_bar_alpha <= 0 or self.boss_hp is None or self.boss_max_hp is None:
            return

        screen_w, screen_h = self.screen_size
        
        bar_w = int(screen_w * 0.5)
        bar_h = 24
        bar_x = (screen_w - bar_w) // 2
        bar_y = 40
        
        bar_surface = pygame.Surface((screen_w, bar_y + bar_h + 30), pygame.SRCALPHA)
        
        border_rect = pygame.Rect(bar_x, bar_y, bar_w, bar_h)
        bg_rect = pygame.Rect(bar_x + 2, bar_y + 2, bar_w - 4, bar_h - 4)
        
        # Black border
        pygame.draw.rect(bar_surface, (0, 0, 0, int(self.boss_bar_alpha)), border_rect, 2)
        # Charcoal background
        pygame.draw.rect(bar_surface, (40, 40, 40, int(self.boss_bar_alpha)), bg_rect)
        
        # Solid Red bar
        health_ratio = max(0.0, min(1.0, self.boss_hp / self.boss_max_hp))
        if health_ratio > 0:
            fill_w = int((bar_w - 4) * health_ratio)
            fill_rect = pygame.Rect(bar_x + 2, bar_y + 2, fill_w, bar_h - 4)
            pygame.draw.rect(bar_surface, (230, 0, 0, int(self.boss_bar_alpha)), fill_rect)

        # Title centered above the bar
        title_text = FONT.render("The Dwarf King", True, (255, 255, 255))
        title_text.set_alpha(int(self.boss_bar_alpha))
        title_rect = title_text.get_rect(center=(screen_w // 2, bar_y - 20))
        bar_surface.blit(title_text, title_rect)
        
        # Values centered inside the bar
        hp_str = f"{self.boss_hp}/{self.boss_max_hp}"
        hp_text = FONT_SMALL.render(hp_str, True, (255, 255, 255))
        hp_text.set_alpha(int(self.boss_bar_alpha))
        hp_rect = hp_text.get_rect(center=(screen_w // 2, bar_y + bar_h // 2))
        bar_surface.blit(hp_text, hp_rect)
        
        screen.blit(bar_surface, (0, 0))