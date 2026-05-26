from serv.domain.mob.mob import Mob
from serv.config import monster_info
from serv.domain.weapon import weapon1
from serv.domain.mob.team import Team
from shared.constants import world
from serv.domain.projectile import projectile_type
import math,time,random

class Monster(Mob):
    def __init__(self, hp, damage, x, y,rad=15, atk_rad=2, atk_speed=1,run_away = -1, id = None,prime = 10,acceleration = 0.2,width = 10,height = 10,knockback_res = 0,len_life = 0):

        super().__init__((x,y),hp,id,acceleration=acceleration,height = height,width = width)

        self.time_destroy = time.perf_counter()+len_life
        if len_life != 0:
            self.auto_destruction = True

        self.player_did_dammage = {}

        self.hp = hp
        self.damage = damage
        self.resist = False #Resist = ne peut pas subir de dégâts
        #Résistance au knockback : soustraite au knockback reçu. toujours entre [0,3] (0 = aucune résistance)
        self.knockback_res = max(0, min(3, knockback_res))
        self.prime = prime

        self.side = "right"#0 right, 1 = left
        
        self.attack_radius = atk_rad
        self.attack_speed = atk_speed
        self.run_away_rad = run_away

        self.collision_damage = True
        self.collision_atk = 10
        self.collision_time_reload = 0.5
        self.collision_start = time.perf_counter()
        self.collision_damage = True

        self.radius = rad

        self.target = None #Met la cible à None
        self.dist = 0 #Distance jusqu'au joueur ciblé

        self.focus = False #Focus = ne change pas d'état

        self.state = "idle"  # états possibles : idle, moving, attacking, dead

    def move_left(self,map,dt,force_move=False):

        if force_move :
            super().move_left(dt)
        
        else :
            delta_y = self.half_height + self.base_movement
            delta_x = -(self.half_width+self.base_movement)
            if self.touch_type(0,delta_x,map,map.dur) : #y puis x
                self.side = "right"

            elif self.touch_type(delta_y,delta_x,map,map.vide):
                self.side = "right"
            
            else :
                super().move_left(dt)

    def move_right(self,map,dt,force_move = False):

        if force_move :
            super().move_right(dt)

        else :
            delta_y = self.half_height + self.base_movement
            delta_x = self.half_width+self.base_movement
            if self.touch_type(0,delta_x,map,map.dur) : #y puis x
                self.side = "left"

            elif self.touch_type(delta_y,delta_x,map,map.vide):
                self.side = "left"
            
            else :
                super().move_right(dt)

    def is_alive(self):
        return self.hp>0
    
    def has_to_destroy(self):
        if self.auto_destruction :
            return time.perf_counter()>=self.time_destroy
        return False

    def has_line_of_sight(self, map, target):
        x0, y0 = self.pos_x, self.pos_y
        x1, y1 = target.pos_x, target.pos_y
        dx = x1 - x0
        dy = y1 - y0
        dist = math.hypot(dx, dy)
        if dist == 0:
            return True
        
        step_x = dx / dist * self.base_movement
        step_y = dy / dist * self.base_movement
        
        steps = int(dist // self.base_movement)
        
        curr_x, curr_y = x0, y0
        for _ in range(steps):
            bx = self.convert_to_base(curr_x)
            by = self.convert_to_base(curr_y)
            try:
                cell_type = map.return_type(by, bx)
                if self.is_type(cell_type, map.dur):
                    return False
            except Exception:
                pass
            curr_x += step_x
            curr_y += step_y
        return True

    def distance_to_nearest_player(self, lPlayer,friendly_monsters = [],map = None,chunk = None):
        """Distance euclidienne en cases entre le monstre et le joueur."""
        target = None
        best = None
        for p in lPlayer.values():
            #if not self.has_line_of_sight(map, p): #Issue come from here ?
            #    continue
            dx = p.pos_x - self.pos_x
            dy = p.pos_y - self.pos_y
            d = math.hypot(dx, dy)
            if best is None or d < best:
                best = d
                target = p
        for m in friendly_monsters[chunk]:
            #if not self.has_line_of_sight(map, p): #Issue come from here ?
            #    continue
            dx = m.pos_x - self.pos_x
            dy = m.pos_y - self.pos_y
            d = math.hypot(dx, dy)
            if best is None or d < best:
                best = d
                target = m

        if target is None:
            #print("None ! why ",lPlayer.values())
            return None, float("inf")
        
        return target, best / self.base_movement
    
    def dist_to_target_player(self,player):
        """Retourne la distance jusqu'au joueur ciblé"""

        dx = player.pos_x - self.pos_x
        dy = player.pos_y - self.pos_y
        d = math.hypot(dx, dy)
        
        return d/self.base_movement
    # --- Boucle de comportement basique pour tous les monstres ---

    def update(self,map,dt,lPlayer,friendly_monsters,collision_handler,chunk):
        
        self.target, self.dist = self.distance_to_nearest_player(lPlayer,friendly_monsters,map,chunk)

        if not self.is_alive():
            self.state = "dead"
            return
            
        if self.state == "stunned":
            if time.perf_counter() > getattr(self, 'stun_timer', 0):
                self.state = "idle"
                #self.target = None #Fis issue
            else:
                return

        #if self.target == None : #Set the target and change only if has no target
        #else :
        #    self.dist = self.dist_to_target_player(self.target) #If already has a target, just update the dist

        #------------degat de collision-----------------#
        if self.dist<self.width/2/self.base_movement and self.collision_damage: 

            if self.collision_start + self.collision_time_reload <= time.perf_counter():
                self.collision_start=time.perf_counter()

                if not self.target.auto_destruction :
                    chunk = 99
                collision_handler.player_take_damage_no_projectile(self.collision_atk,self.target,chunk)
            #FIn

        if self.focus :
            return

        elif self.state == "idle":
            if self.dist<= self.attack_radius :
                self.state = "attacking"

            if self.dist <= self.radius:
                self.state = "moving"
       
        elif self.state == "attacking":
            if self.dist > self.attack_radius:
               # Revenir à l'état de déplacement si le joueur s'éloigne
                self.state = "moving"
            elif self.dist <= self.run_away_rad:
                # Fui car ennemy trop proche. Si pas cette up, jamais declenché
                self.state = "run away"

        elif self.state == "moving":
            if self.dist <= self.run_away_rad :
                self.state = "run away"
            if self.dist <= self.attack_radius:
                self.state = "attacking"
            elif self.dist > self.radius * 1.2:
                self.state = "idle"
                self.target = None #Reset de l'aggro

        elif self.state == "run away":

            #if self.dist > self.run_away_rad :

            if self.dist > self.radius :
                self.state = "moving"

            if self.dist >= self.run_away_rad +15 or self.dist < (self.width/2)/self.base_movement : #0 = delta
                self.state = "attacking"


    def take_damage(self, amount,player_did_damage=None,knockback=0):
        """Retourne True/False selon si le monstre est mort ou non.
        knockback : force du recul (0 = aucun), définie par l'arme ou le sort."""

        if self.dead:
            return False

        if amount!=0 :

            if self.resist :
                amount = 0 #Le met a 0 comme ca envoie quand mm cote client le 0 => dessine "bloque"

            self.life -= amount
            self.send_new_life = True

            self.player_did_dammage[player_did_damage] = time.perf_counter()

            #Knockback seulement si l'arme ou le sort en a un, réduit par la résistance du monstre
            effective_kb = max(0, knockback - self.knockback_res)

            if player_did_damage!=None and effective_kb and hasattr(player_did_damage, 'pos_x'):
                dx = self.pos_x - player_did_damage.pos_x
                dir = 1 if dx > 0 else -1
                self.vitesse_x = dir * self.base_movement * 15 * effective_kb
                self.vitesse_y = -self.base_movement * 5 * effective_kb
                
            #Étourdi seulement quand le knockback réellement subi dépasse 1.5
            #if effective_kb > 1.5: #I remove it bcs pour le defendeur en gros il doit se poser 2 sec avant de retaper mais dcp avec le stun, si on le tape il nous tape direct après
            #    self.state = "stunned"
            #    self.stun_timer = time.perf_counter() + 0.2

            #self.focus = False #Why ???

            if self.life <= 0:
                self.life = 0
                self.die()

                return True

        return False
    
    def die(self):

        for player,time_damage in self.player_did_dammage.items() :

            if player!=None and player.team == Team.Player and time_damage+5 > time.perf_counter():
                player.update_money(self.prime)

        self.player_did_dammage.clear()
        self.dead = True
        self.target = None
        self.start_dead = time.perf_counter()

    def still_dead(self):

        if not self.dead :
            return False

        if self.start_dead+self.len_dead < time.perf_counter():
            self.respawn()

        return self.dead

    def respawn(self):
        self.dead = False
        self.focus = False
        self.state = "idle"
        self.full_heal()

    def get_angle(self, player):
        adjacent = player.pos_x - self.pos_x
        opp = -((player.pos_y ) - self.pos_y)  # négatif !

        angle = math.atan2(opp, adjacent)
        angle = angle * 180 / math.pi

        return int(angle) % 360

    def check_if_player_collide_attack(self,target,side,hit_box_damage_width):

        #Test en y :
        if target.pos_y-target.half_height > self.pos_y + self.half_height or target.pos_y + target.half_height < self.pos_y - self.half_height :
            return False

        if side == "right":
            if self.pos_x + hit_box_damage_width*self.base_movement < target.pos_x-target.half_width or self.pos_x > target.pos_x + target.half_width :
                return False
            
        if side == "left":
            if self.pos_x - hit_box_damage_width*self.base_movement > target.pos_x+target.half_width or self.pos_x < target.pos_x - target.half_width :
                return False
            
        return True


    # --- Déplacement pour gestion des collisions ---

    # Vérifie si une cellule est bloquante (dure ou liquide)


    # Essayer de déplacer le monstre selon l'axe X en gérant les collisions


    # Essayer de déplacer le monstre selon l'axe Y en gérant les collisions

    
    # Vérifie si le monstre chevauche une cellule dure


    # Essayer de monter d'une cellule si possible lors d'un déplacement horizontal

#Creation specifique de chaque monstre

class Laseroide(Monster) :

    def __init__(self,x,y,id = 0):

        super().__init__(hp=40+5*world.NBR_OF_PLAYER,damage = 5,x=x,y=y,atk_rad = monster_info.LASEROIDE_ATK_RAD,rad = monster_info.LASEROIDE_RAD,run_away = monster_info.LASEROIDE_TOO_CLOSE,atk_speed = 1,id=id,prime =30,acceleration = monster_info.LASEROIDE_ACCELERATION,height = 8)

        self.acceleration_y = 20* self.acceleration
        self.knockback_res = 0 #Resist pas

        self.name = 1 #Permet d'affihcer le bon monstre
        self.weapon = weapon1.WeaponLaseroide(team = self.team,player = self)

        self.last_time_jump = time.perf_counter()
        self.begin_shot = time.perf_counter()
        self.time_before_shot = 1
        self.angle = 0
        self.begin_relax = time.perf_counter()
        self.time_relax = 1.5

    def update(self, map, lPlayer,friendly_monsters,dt,collision_handler,projectile_manager,chunk):

        if self.still_dead():
            return
        
        super().update(map,dt,lPlayer,friendly_monsters,collision_handler,chunk)

       # --- Deplacement selon l'état ---
        if self.state == "idle":
            self.idle_behavior(map,dt)
            
        elif self.state == "moving":
            self.moving_behavior(self.target, map,dt)

        elif self.state == "run away":
            self.leave_behavior(self.target,map,dt)
            
        elif self.state == "attacking":
            if not self.focus : 
                self.state = "loading"
                self.focus = True
                self.angle = self.get_angle(self.target)
                self.begin_shot = time.perf_counter()
                self.vitesse_x = 0
                if self.angle > 90 and self.angle < 270:
                    self.side = "left"
                else:
                    self.side = "right"

            else :
                self.attack(self.target,collision_handler,dt,projectile_manager)

        elif self.state == "loading" :
            if self.begin_shot+self.time_before_shot <= time.perf_counter() :
                self.state = "attacking"

        delta = self.move_all(map,dt,collision_handler)

        if not self.focus :
            self.check_if_jump(delta,map)

    def check_if_jump(self,delta,map):

        if delta[0]==0 and (self.state == "run away" or self.state=="moving") and self.last_time_jump+1 < time.perf_counter():
            if self.jump(map): #si réussi
                self.last_time_jump = time.perf_counter()

        elif delta[1]>0 and self.last_time_jump+1 < time.perf_counter() :
            if self.jump(map): #si réussi
                self.last_time_jump = time.perf_counter()

        elif delta[0]!=0:
            self.last_time_jump = time.perf_counter()

    def idle_behavior(self,map,dt):
        """Reste sur place"""
        if self.focus :
            if self.time_relax + self.begin_relax <= time.perf_counter():
                self.focus = False
                self.state = "moving"
                self.last_time_jump = time.perf_counter()#Prevent jump

        return
    
    def moving_behavior(self,target,map,dt):
        """Se déplace vers le joueur"""
        if target.pos_x<self.pos_x :
            self.side = "left"
            self.move_left(map,dt)
        
        else :
            self.side = "right"
            self.move_right(map,dt)
    
    def leave_behavior(self,target,map,dt):
        """Se déplace à l'opposé du joueur"""
        if target.pos_x<self.pos_x :
            self.side = "right"
            self.move_right(map,dt)
        
        else :
            self.side = "left"
            self.move_left(map,dt)

    def attack(self,target,collision_handler,dt,projectile_manager):
        
        infos = self.weapon.trigger_shot(self.angle,(self.pos_x,self.pos_y))

        if infos != None :

            projectiles,_,_ = infos

            for proj in projectiles :

                projectile_manager.add_projectile_create(proj)

        if self.weapon.idx == 0:
            #self.focus = True
            self.state = "idle"
            self.begin_relax = time.perf_counter()

class Foulli(Monster) :

    def __init__(self,x,y,id=0):

        super().__init__(hp=10,damage=10,x=x,y=y,atk_rad = monster_info.FOULLI_ATTAQUE_RAD,atk_speed = 1,id=id,prime = 5,acceleration = 0,width = 6,height = 6)

        self.knockback_res = 10

        self.name = 2 #Permet d'afficher le bon monstre / Dans monster all côté client
        self.weapon = weapon1.WeaponLaseroide(team = self.team,player = self)

        self.begin_shot = time.perf_counter()
        self.time_before_shot = 0.3
        self.time_after_shot = 0.5

        self.collision_damage = False

    def update(self, map, lPlayer,friendly_monsters,dt,collision_handler,projectile_manager,chunk):

        if self.still_dead():
            return
        
        super().update(map,dt,lPlayer,friendly_monsters,collision_handler,chunk)

       # --- Deplacement selon l'état ---
        if self.state == "idle":
            self.idle_behavior(map,dt)
            
        elif self.state == "moving":
            self.moving_behavior(self.target, map,dt)
            
        elif self.state == "attacking":
            if not self.focus :
                self.focus = True
                self.state = "loading"
                self.begin_shot = time.perf_counter()
            
            else :

                if self.begin_shot + self.time_after_shot <= time.perf_counter() :
                    self.state = "idle"
                    self.focus = False

        elif self.state == "loading" :
            if self.begin_shot+self.time_before_shot <= time.perf_counter() :
                self.state = "attacking"
                self.begin_shot = time.perf_counter()
                if self.dist <=self.attack_radius :
                    self.attack(self.target,collision_handler,dt,projectile_manager,chunk)

        delta = self.move_all(map,dt,collision_handler)

    def idle_behavior(self,map,dt):
        """Reste sur place"""
        return
    
    def moving_behavior(self,target,map,dt):
        """Se déplace vers le joueur"""
        return
    
    def leave_behavior(self,target,map,dt):
        """Se déplace vers le joueur"""
        return

    def attack(self,target,collision_handler,dt,projectile_manager,chunk):
        
        if not self.target.auto_destruction :
            chunk = 99

        collision_handler.player_take_damage_no_projectile(self.damage,self.target,chunk)

class Defendeur(Monster) :

    def __init__(self,x,y,id=0):

        super().__init__(hp=10+10*world.NBR_OF_PLAYER,damage =5,x=x,y=y,atk_rad = monster_info.DEFENDEUR_ATK_RAD,rad = monster_info.DEFENDEUR_RAD,run_away = monster_info.DEFENDEUR_TOO_CLOSE,atk_speed = 1,id=id,prime = 30,acceleration = monster_info.DEFENDEUR_ACCELERATION,width = 5,height = 8)

        self.name = 3 #Permet d'afficher le bon monstre / Dans monster all côté client
        self.knockback_res = 3
        #self.weapon = weapon1.WeaponLaseroide(team = self.team,player = self)

        self.begin_attack = time.perf_counter()
        self.time_for_move_to_reach_player = 0.3
        self.len_attack = 1
        self.begin_time_for_attack = time.perf_counter()
        self.time_between_attacks = 0.2

        self.begin_relax = time.perf_counter()
        self.time_to_relax = 1.5
        self.hit_box_damage_width = 5
        self.resist = True

        #self.collision_damage = False

    def update(self, map, lPlayer,friendly_monsters,dt,collision_handler,projectile_manager,chunk):

        if self.still_dead():
            return
        
        super().update(map,dt,lPlayer,friendly_monsters,collision_handler,chunk)

       # --- Deplacement selon l'état ---
        if self.state == "idle":
            self.idle_behavior(map,dt)
            
        elif self.state == "moving":

            if self.focus :
                if self.begin_attack + self.time_for_move_to_reach_player > time.perf_counter() :

                    if self.check_if_player_collide_attack(self.target,self.side,2) :
                        self.state = "attacking"
                        #self.resist = False #here if too difficult
                        self.begin_attack = time.perf_counter()-self.time_for_move_to_reach_player

                    if self.side == "right":
                        self.move_right(map,dt)
                    else :
                        self.move_left(map,dt)

                else :
                    self.state = "attacking"
                    #self.resist = False# Here if too difficult

            else :

                self.moving_behavior(self.target, map,dt)
            
        elif self.state == "attacking":

            if not self.focus :
                self.focus = True
                self.resist = True
                self.begin_attack = time.perf_counter()

                self.state = "moving"

            if self.focus :
            
                if self.begin_attack+self.len_attack <= time.perf_counter() : #Signifie arrêter l'attaque

                    self.begin_relax = time.perf_counter()
                    self.resist = False
                    self.state = "idle"

                if self.begin_time_for_attack + self.time_between_attacks < time.perf_counter():

                    if self.pos_x < self.target.pos_x : #Définit le côté de l'attaque
                        if self.side != "right":
                            self.side = "right"
                    else :
                        if self.side != "left":
                            self.side = "left"

                    self.attack(self.target,collision_handler,dt,projectile_manager,chunk)
                    self.begin_time_for_attack = time.perf_counter()

        delta = self.move_all(map,dt,collision_handler)

    def idle_behavior(self,map,dt):
        """est épuisé"""
        if self.focus :
            if self.time_to_relax + self.begin_relax <= time.perf_counter():
                self.focus = False
                self.resist = True
                #self.state = "moving"
    
    def moving_behavior(self,target,map,dt):
        """Se déplace vers le joueur"""

        if target.pos_x<self.pos_x :
            self.move_left(map,dt)
        
        else :
            self.move_right(map,dt)
    
    def leave_behavior(self,target,map,dt):
        """Se déplace vers le joueur"""
        if target.pos_x<self.pos_x :
            self.move_right(map,dt)
        
        else :
            self.move_left(map,dt)

    def attack(self,target,collision_handler,dt,projectile_manager,chunk):
        """Retourne True si le joueur est bien touché"""
        
        if self.check_if_player_collide_attack(self.target,self.side,self.hit_box_damage_width) :
            if not self.target.auto_destruction :
                chunk = 99
            collision_handler.player_take_damage_no_projectile(self.damage,self.target,chunk)
            return True
        
        return False

class Escargot(Monster) :

    def __init__(self,x,y,id=0):

        super().__init__(hp=10+5*world.NBR_OF_PLAYER,damage =5,x=x,y=y,atk_rad = monster_info.ESCARGOT_ATK_RAD,rad = monster_info.ESCARGOT_RAD,run_away = monster_info.ESCARGOT_TOO_CLOSE,atk_speed = 1,id=id,prime = 10,acceleration = monster_info.ESCARGOT_ACCELERATION,width = 6,height = 6)

        self.knockback_res = 0.5

        self.name = 4 #Permet d'afficher le bon monstre / Dans monster all côté client

        #self.collision_damage = False

    def update(self, map, lPlayer,friendly_monsters,dt,collision_handler,projectile_manager,chunk):

        if self.still_dead():
            return
        
        #print(self.state)
        
        super().update(map,dt,lPlayer,friendly_monsters,collision_handler,chunk)

       # --- Deplacement selon l'état ---
        if self.state == "idle":
            self.idle_behavior(map,dt)
            
        elif self.state == "moving":

            self.moving_behavior(self.target, map,dt)
            
        elif self.state == "attacking":

            self.attack(self.target,collision_handler,dt,projectile_manager)

        delta = self.move_all(map,dt,collision_handler)

    def idle_behavior(self,map,dt):
        """est épuisé"""
        self.state = "moving"
    
    def moving_behavior(self,target,map,dt):
        """Se déplace vers le joueur"""

        if self.side == "right":
            
            self.move_right(map,dt)

        elif self.side == "left":

            self.move_left(map,dt)
    
    def leave_behavior(self,target,map,dt):
        """Se déplace vers le joueur"""

    def attack(self,target,collision_handler,dt,projectile_manager):
        """Retourne True si le joueur est bien touché"""
        #self.state = "moving"

class Mma(Monster) :

    def __init__(self,x,y,id=0):

        super().__init__(hp=30+20*world.NBR_OF_PLAYER,damage =6,x=x,y=y,atk_rad = monster_info.MMA_ATK_RAD,rad = monster_info.MMA_RAD,run_away = monster_info.MMA_TOO_CLOSE,atk_speed = 1,id=id,prime = 40,acceleration = monster_info.MMA_ACCELERATION,width = 8,height = 8)

        self.knockback_res = 0.5

        self.name = 9 #Permet d'afficher le bon monstre / Dans monster all côté client

        self.last_attack = time.perf_counter()
        self.len_for_1_attack = 0.1
        self.min_time_move = 1
        self.begin_min_time_move = time.perf_counter()

        self.hit_box_damage_width = 8
        self.collision_atk = 5

        self.begin_attack = time.perf_counter()
        self.len_attack = 1.5
        self.begin_relax = time.perf_counter()
        self.time_relax = 0.8

        #self.collision_damage = False

    def update(self, map, lPlayer,friendly_monsters,dt,collision_handler,projectile_manager,chunk):

        if self.still_dead():
            return
        
        #print(self.state)
        
        super().update(map,dt,lPlayer,friendly_monsters,collision_handler,chunk)

       # --- Deplacement selon l'état ---
        if self.state == "idle":
            self.idle_behavior(map,dt)
            
        elif self.state == "moving":

            self.moving_behavior(self.target, map,dt)
            
        elif self.state == "attacking":

            self.attack(collision_handler,map,dt)

        elif self.state =="jump" :
            self.jump_behavior(self.target,map,dt)

        elif self.state =="fall" :
            self.fall_behavior(self.target,map,dt)

        self.move_all(map,dt,collision_handler)

    def idle_behavior(self,map,dt):
        """est épuisé"""

        if not self.focus :
            if self.side == "right":
                
                self.move_right(map,dt)

            elif self.side == "left":

                self.move_left(map,dt)

        else :
            if self.begin_relax + self.time_relax < time.perf_counter():
                self.begin_min_time_move = time.perf_counter()
                self.state = "moving"
    
    def moving_behavior(self,target,map,dt):
        """Se déplace vers le joueur"""

        if self.focus :
            if self.min_time_move + self.begin_min_time_move < time.perf_counter():
                self.focus = False

        if target.pos_x < self.pos_x :
            self.side = "left"
            self.move_left(map,dt,True)
        else :
            self.side = "right"
            self.move_right(map,dt,True)

        if self.target.pos_y > self.pos_y +self.half_height:
            self.is_climbing = False
            self.move_down(dt)

        elif self.target.pos_y < self.pos_y - self.half_height:
            self.jump(dt)

        else :
            self.is_climbing=True

    def jump_behavior(self,target,map,dt):

        if self.vitesse_y>0:
            self.state = "fall"

        if target.pos_x < self.pos_x :
            self.side = "left"
            self.move_left(map,dt,True)
        else :
            self.side = "right"
            self.move_right(map,dt,True)

    def fall_behavior(self,target,map,dt):

        if self.vitesse_y==0:
            self.state = "attacking"
            self.begin_attack = time.perf_counter()

        if target.pos_x < self.pos_x :
            self.side = "left"
            self.move_left(map,dt,True)
        else :
            self.side = "right"
            self.move_right(map,dt,True)
    
    def leave_behavior(self,target,map,dt):
        """Se déplace vers le joueur"""

    def attack(self,collision_handler,map,dt):
        """Retourne True si le joueur est bien touché"""
        if not self.focus : 
            self.focus = True
            self.state = "jump"
            self.jump(map)

        else :

            if self.target.pos_y > self.pos_y +self.half_height:
                self.is_climbing = False
                self.move_down(dt)

            elif self.target.pos_y < self.pos_y - self.half_height:
                self.jump(dt)

            else :
                self.is_climbing=True

            if self.begin_attack+self.len_attack<time.perf_counter():
                self.state = "idle"
                self.begin_relax = time.perf_counter()
            
            elif self.last_attack + self.len_for_1_attack <= time.perf_counter():
                self.last_attack = time.perf_counter()
                if self.target.pos_x<self.pos_x:
                    self.side = "left"
                else :
                    self.side = "right"

                if self.check_if_player_collide_attack(self.target,self.side,self.hit_box_damage_width) :
                    if not self.target.auto_destruction :
                        chunk = 99
                    collision_handler.player_take_damage_no_projectile(self.damage,self.target,chunk)

class Shaman(Monster) :

    def __init__(self,x,y,id=0):

        super().__init__(hp=10+15*world.NBR_OF_PLAYER,damage =6,x=x,y=y,atk_rad = monster_info.SHAMAN_ATK_RAD,rad = monster_info.SHAMAN_RAD,run_away = monster_info.SHAMAN_TOO_CLOSE,atk_speed = 1,id=id,prime = 40,acceleration = monster_info.SHAMAN_ACCELERATION,width = 8,height = 8)

        self.knockback_res = 0

        self.name = 10 #Permet d'afficher le bon monstre / Dans monster all côté client

        self.projecitles = [projectile_type.Death]
        self.has_shot = False

        self.begin_shot = time.perf_counter()
        self.time_before_shot = 1
        self.angle = 0

        self.begin_relax = time.perf_counter()
        self.time_relax = 0.4

    def update(self, map, lPlayer,friendly_monsters,dt,collision_handler,projectile_manager,chunk):

        if self.still_dead():
            return
        
        super().update(map,dt,lPlayer,friendly_monsters,collision_handler,chunk)

       # --- Deplacement selon l'état ---
        if self.state == "idle":
            self.idle_behavior(map,dt)
            
        elif self.state == "moving":
            self.moving_behavior(self.target, map,dt)

        elif self.state == "run away":
            self.leave_behavior(self.target,map,dt)
            
        elif self.state == "attacking":
            if not self.focus : 
                self.state = "loading"
                self.focus = True
                self.begin_shot = time.perf_counter()
                self.vitesse_x = 0
                if self.angle > 90 and self.angle < 270:
                    self.side = "left"
                else:
                    self.side = "right"

            else :
                self.attack(self.target,collision_handler,dt,projectile_manager)

        elif self.state == "loading" :
            if self.begin_shot+self.time_before_shot <= time.perf_counter() :
                self.state = "attacking"

        self.move_all(map,dt,collision_handler)

    def idle_behavior(self,map,dt):
        """Reste sur place"""

        if self.target.pos_x<self.pos_x :
            self.side = "left"
            self.move_left(map,dt)
        
        else :
            self.side = "right"
            self.move_right(map,dt)
    
    def moving_behavior(self,target,map,dt):
        """Se déplace vers le joueur"""
        if target.pos_x<self.pos_x :
            self.side = "left"
            self.move_left(map,dt)
        
        else :
            self.side = "right"
            self.move_right(map,dt)
    
    def leave_behavior(self,target,map,dt):
        """Se déplace à l'opposé du joueur"""
        if target.pos_x<self.pos_x :
            self.side = "right"
            self.move_right(map,dt)
        
        else :
            self.side = "left"
            self.move_left(map,dt)

    def attack(self,target,collision_handler,dt,projectile_manager):
        
        if not self.has_shot :
            angle = self.get_angle(self.target)
            pos = [self.pos_x,self.pos_y]
            speed = self.half_height
            rad_angle = math.radians(angle)
            x = math.cos(rad_angle)
            y = math.sin(rad_angle)
            pos[0]+=int(x*speed)
            pos[1]+=int(y*speed)

            spell = random.choice(self.projecitles)

            proj = spell(angle,pos,1,False,self)
            proj.load()

            projectile_manager.add_projectile_create(proj)

            self.has_shot = True
            self.begin_relax = time.perf_counter()
        else :
            if self.begin_relax + self.time_relax < time.perf_counter():
                self.state = "moving"
                self.has_shot = False
                self.focus = False

class Wall(Monster) :

    def __init__(self,x,y,id=0):

        super().__init__(hp=20,damage =5,x=x,y=y,atk_rad = 0,rad = 0,run_away = 0,atk_speed = 1,id=id,prime = 0,acceleration = 1,width = 8,height = 8,len_life = 5)

        self.knockback_res = 10
        self.team = Team.Player

        self.name = 7 #Permet d'afficher le bon monstre / Dans monster all côté client

        self.collision_damage = False

    def update(self, map, lPlayer,friendly_monsters,dt,collision_handler,projectile_manager,chunk):

        if self.still_dead():
            return
        
        #print(self.state)
        
        super().update(map,dt,lPlayer,friendly_monsters,collision_handler,chunk)

       # --- Deplacement selon l'état ---
        if self.state == "idle":
            self.idle_behavior(map,dt)
            
        elif self.state == "moving":
            pass
            
        elif self.state == "attacking":
            pass

        self.move_all(map,dt,collision_handler)
        #print(s)

    def idle_behavior(self,map,dt):
        """est épuisé"""

class WallBig(Monster) :

    def __init__(self,x,y,id=0):

        super().__init__(hp=20,damage =5,x=x,y=y,atk_rad = 0,rad = 0,run_away = 0,atk_speed = 1,id=id,prime = 0,acceleration = 1,width = 8,height = 8,len_life = 5)

        self.knockback_res = 10
        self.team = Team.Player

        self.name = 8 #Permet d'afficher le bon monstre / Dans monster all côté client

        self.collision_damage = False

    def update(self, map, lPlayer,friendly_monsters,dt,collision_handler,projectile_manager,chunk):

        if self.still_dead():
            return
        
        #print(self.state)
        
        super().update(map,dt,lPlayer,friendly_monsters,collision_handler,chunk)

       # --- Deplacement selon l'état ---
        if self.state == "idle":
            self.idle_behavior(map,dt)
            
        elif self.state == "moving":
            pass
            
        elif self.state == "attacking":
            pass

        self.move_all(map,dt,collision_handler)
        #print(s)

    def idle_behavior(self,map,dt):
        """est épuisé"""

class Limace(Monster) :
    """Se déplace, tire un projectile de loin, sinon attaque au corps à corps"""

    def __init__(self,x,y,id=0):

        super().__init__(hp=5+5*world.NBR_OF_PLAYER,damage = 5,x=x,y=y,atk_rad = monster_info.LIMACE_ATK_RAD,rad = monster_info.LIMACE_RAD,run_away = monster_info.LIMACE_TOO_CLOSE,atk_speed = 1,id=id,prime = 15,acceleration = monster_info.LIMACE_ACCELERATION,width = 6,height = 6)

        self.name = 5 #Permet d'afficher le bon monstre / In monster all dans client

        self.begin_attack = time.perf_counter()
        self.isMelee = False
        self.norme = 0

        self.melee_radius = 12 #self.attack_radius/3
        self.time_before_melee_attack = 0.3 #0.2

        self.weapon = weapon1.WeaponLimace(team = self.team,player = self)
        self.time_before_range_attack = 1 #0.7
        self.angle = 0

        self.start_cooldown = time.perf_counter()
        self.cooldown = 1.5
        #self.collision_damage = False

    def update(self, map, lPlayer,friendly_monsters,dt,collision_handler,projectile_manager,chunk):

        if self.still_dead():
            return
        
        super().update(map,dt,lPlayer,friendly_monsters,collision_handler,chunk)

        if self.start_cooldown + self.cooldown > time.perf_counter() : #cooldown state after ranged atk (marche)
            self.state = "moving"


       # --- Deplacement selon l'état ---
        if self.state == "idle":
            self.idle_behavior(map,dt)
            
        elif self.state == "moving":
            self.moving_behavior(self.target, map,dt)
            
        elif self.state == "attacking":

            if not self.focus : #1ere boucle

                self.state = "loading" 
                self.focus = True #ne change plus d'état
                self.begin_attack = time.perf_counter() #début de l'attaque

                self.norme = self.dist

                if self.norme <= self.melee_radius : #melee attack
                        self.isMelee = True

                else : #range attack
                    self.angle = self.get_angle(self.target)

                    #print("Focus angle : " + str(self.angle))
                    
                    if self.angle > 90 and self.angle < 270:
                        self.side = "left"
                    else:
                        self.side = "right"

            else :
                if self.isMelee :
                    self.melee_attack(self.target,collision_handler,dt,projectile_manager,chunk)
                    self.isMelee = False

                else :
                    self.range_attack(self.target,collision_handler,dt,projectile_manager)
                    self.start_cooldown = time.perf_counter()

                self.state = "moving" 
                self.focus = False      
        
        elif self.state == "loading" :

            if self.isMelee:
                self.jump(map)
    
                if self.begin_attack + self.time_before_melee_attack <= time.perf_counter() :
                    self.state = "attacking"

            else :
                if self.begin_attack + self.time_before_range_attack <= time.perf_counter() :
                    self.state = "attacking"


        delta = self.move_all(map,dt,collision_handler)

    def idle_behavior(self,map,dt):
        """Juste animation (Regarde autour de lui)"""
        self.focus = False
    
    def moving_behavior(self,target,map,dt):
        """Move to the player"""

        if target.pos_x<self.pos_x :
            self.side = "left"
            self.move_left(map,dt)
        
        else :
            self.side = "right"
            self.move_right(map,dt)
    
    def leave_behavior(self,target,map,dt):
        return
    
    def melee_attack(self,target,collision_handler,dt,projectile_manager,chunk):
        """moves"""
        if not self.target.auto_destruction : 
            chunk = 99
        collision_handler.player_take_damage_no_projectile(self.damage,self.target,chunk)
    
    
    def range_attack(self,target,collision_handler,dt,projectile_manager):

        trigger = self.weapon.trigger_shot(self.angle,(self.pos_x,self.pos_y))

        if trigger != None :

            (projectiles, _,_) = trigger

            for proj in projectiles :
                projectile_manager.add_projectile_create(proj)

        if self.weapon.idx == 0:
            self.focus = False
            self.state = "moving"

class Skeleton(Monster):

    def __init__(self, x, y, id=0):
        super().__init__(hp=20+5*world.NBR_OF_PLAYER, damage=10, x=x, y=y, rad=30, atk_rad=5, atk_speed=1, id=id,prime = 20)
        
        self.knockback_res = 1

        self.name = 0
        
        #valeurs par défaut de l'état idle, peuvent changer selon le monstre
        self.direction = 1
        self.idle_min_x = x - 30 *self.base_movement
        self.idle_max_x = x + 30 *self.base_movement
        
        #vitesse différente selon l'état
        self.speed_idle = max(1, self.base_movement * 8)
        self.speed_chase = max(1, self.base_movement * 5)
        self.speed_max = max(1, self.base_movement * 6)
        
        #pour le stepup et le no turn lors de l'idle
        self.step_lock = 0
        self.no_turn = 0
        self.idle_stuck = 0

    def update(self, map, lPlayer,friendly_monsters,dt,collision_handler,projectile_manager,chunk):

        if self.still_dead():
            return
        
        super().update(map,dt,lPlayer,friendly_monsters,collision_handler,chunk)
       # --- Deplacement selon l'état ---
        if self.state == "idle":
            self.idle_behavior(map,dt)
            
        elif self.state == "moving":
            self.moving_behavior(lPlayer, map,dt)
            
        elif self.state == "attacking":
            self.attack(self.target,collision_handler,dt,chunk)
        elif self.state == "stunned":
            self.gravity_effect(dt)
            self.collision_x(map, dt, self.vitesse_x)
            self.collision_y(map, dt, self.vitesse_y)
            self.update_vitesse(dt)
    
    def can_walk_on(self, cells_arr, new_x, new_y, cell_dur, cell_vide, cell_liquid):
        
        bx = int(new_x // self.base_movement)
        by = int(new_y // self.base_movement)

        h = len(cells_arr)
        w = len(cells_arr[0]) if h else 0
            # check si hors map
        if bx < 0 or by < 0 or bx >= w or by >= h:
            return False

        cell_type = cells_arr[by][bx]
        if self.is_type(cell_type, cell_dur):
            return True                                    # peut marcher sur les cellules dures
        if self.is_type(cell_type, cell_liquid):
            return False                                   # ne peut pas marcher sur les liquides
        return True                                        # peux marcher sur les autres cellules (vides, sols)
        
        #--- Comportements spécifiques ---
        
    #comportement en mode idle : patrouille entre deux points fixes
    def idle_behavior(self, map,dt):
        intended_vx = self.direction * self.speed_idle
        if intended_vx == 0:
            intended_vx = self.direction * max(1, self.base_movement // 8)

        if self.pos_x + intended_vx < self.idle_min_x or self.pos_x + intended_vx > self.idle_max_x:
            self.direction *= -1
            intended_vx = self.direction * max(1, self.base_movement // 8)

        self.gravity_effect(dt)

        self.vitesse_x = intended_vx
        moved_x = self.collision_x(map,dt,self.vitesse_x)
        self.collision_y(map,dt,self.vitesse_y)

        if moved_x == 0 and intended_vx != 0:
            stepped = self.try_step_up_1(map, intended_vx,dt)
            if stepped != 0:
                self.step_lock = 4
                self.no_turn = 6
                moved_x = stepped
                self.vitesse_x = intended_vx
                self.collision_x(map,dt,self.vitesse_x)
            self.collision_y(map,dt,self.vitesse_y)

        if moved_x == 0:
            self.idle_stuck += 1
        else:
            self.idle_stuck = 0

        if self.step_lock > 0:
            self.step_lock -= 1
        if self.no_turn > 0:
            self.no_turn -= 1

        if moved_x == 0:
            if self.idle_stuck >= 10:
                self.direction *= -1
                self.idle_stuck = 0
                self.no_turn = 0
                self.step_lock = 0
            elif self.no_turn == 0 and self.step_lock == 0:
                self.direction *= -1
                
    # comportement en mode moving : poursuite du joueur le plus proche      
    def moving_behavior(self, lPlayer, map,dt):

        if self.target is None:
            return

        dx = self.target.pos_x - self.pos_x
        if abs(dx) < self.base_movement // 10:
            intended_vx = 0
        else:
            intended_vx = self.speed_max if dx > 0 else -self.speed_max

        self.gravity_effect(dt)
        self.vitesse_x = intended_vx
        moved_x = self.collision_x(map,dt,self.vitesse_x)
        self.collision_y(map,dt,self.vitesse_y)
        
        if moved_x == 0 and intended_vx != 0:
            stepped = self.try_step_up_1(map, intended_vx,dt)
            if stepped != 0:
                self.step_lock = 4
                self.no_turn = 6
                moved_x = stepped
                self.vitesse_x = intended_vx
                self.collision_x(map,dt,self.vitesse_x)
            self.collision_y(map,dt,self.vitesse_y)
        
        if self.step_lock > 0:
            self.step_lock -= 1

        if self.no_turn > 0:
            self.no_turn -= 1
            
        if intended_vx != 0:
            self.direction = 1 if intended_vx > 0 else -1
            
    # attaque le joueur le plus proche    
    def attack(self, Player,collision_handler,dt,chunk):
        damage = int(self.damage*10 * dt) #= inflige self.damage en 1 seconde
        if not self.target.auto_destruction :
            chunk = 99
        collision_handler.player_take_damage_no_projectile(damage,Player,chunk)

class DwarfKing(Monster):
    """Boss : Le Roi Nain.
    Très gros et résistant, immunisé au knockback, il poursuit les joueurs,
    invoque des monstres, et esquive avec un dash et un double saut comme un joueur.
    (Les joueurs sont des nains : le boss leur ressemble beaucoup.)"""

    def __init__(self, x, y, id=0):

        super().__init__(
            hp = 500 + 400 * world.NBR_OF_PLAYER,
            damage = monster_info.DWARF_KING_DAMAGE,
            x = x, y = y,
            atk_rad = monster_info.DWARF_KING_ATK_RAD,
            rad = monster_info.DWARF_KING_RAD,
            run_away = -1,                              #N'a jamais peur
            atk_speed = 1,
            id = id,
            prime = monster_info.DWARF_KING_PRIME,
            acceleration = monster_info.DWARF_KING_ACCELERATION,
            width = monster_info.DWARF_KING_WIDTH,
            height = monster_info.DWARF_KING_HEIGHT,
            knockback_res = 3,                          #Immunisé au knockback (résistance max)
        )

        self.name = 6                                   #Texture côté client (joueur, temporaire)
        #self.auto_destruction = True

        # Habiliter le double saut pour la classe SmoothJump du boss
        self.smooth_jump.double_jump = True

        #Dégâts de contact : toucher le boss fait très mal
        self.collision_atk = monster_info.DWARF_KING_DAMAGE
        self.collision_time_reload = 0.7

        #Vitesse de poursuite du joueur
        self.speed_chase = max(1, self.base_movement * 6)

        #Esquive : alterne un dash et un double saut
        self.dodge_cooldown = monster_info.DWARF_KING_DODGE_COOLDOWN
        self.last_dodge = time.perf_counter()
        self.dodge_with_dash = True
        self.dash_until = 0                             #Tant que time < dash_until, on garde la vitesse du dash
        self.double_jump_pending = False
        self.double_jump_time = 0

        #Invocation de monstres (squelettes et laseroïdes)
        self.spawn_cooldown = monster_info.DWARF_KING_SPAWN_COOLDOWN
        self.last_spawn = time.perf_counter()
        self.minions_spawned = 0
        self.max_minions = monster_info.DWARF_KING_MAX_MINIONS
        self.monsters_to_spawn = []                     #Vidé par Read_monster à chaque frame
        self.active_minions = []                        #Liste locale pour limiter les invocations actives

    def update(self, map, lPlayer, friendly_monsters,dt, collision_handler, projectile_manager,chunk):

        if self.still_dead():
            return

        #Gère la cible, la distance, les dégâts de contact et la machine à états
        super().update(map, dt, lPlayer,friendly_monsters,collision_handler,chunk)

        self.try_spawn_minions()
        self.try_dodge(map)
        self.resolve_double_jump(map)

        self.move_boss(map, dt)

    def move_boss(self, map, dt):
        """Déplacement physique : poursuit le joueur, sauf pendant un dash où on laisse filer la vitesse."""

        chasing = self.target is not None and self.state in ("moving", "attacking", "run away")
        now = time.perf_counter()

        if now >= self.dash_until and chasing:
            dx = self.target.pos_x - self.pos_x
            if abs(dx) < self.base_movement:
                self.vitesse_x = 0
            else:
                self.vitesse_x = self.speed_chase if dx > 0 else -self.speed_chase

        if self.vitesse_x < 0: #Change direction du boss en fct de ou il bouge
            self.side = "left"
        else :
            self.side = "right"

        self.gravity_effect(dt)

        pos_before_x = self.pos_x
        self.collision_x(map, dt, self.vitesse_x)
        moved_x = self.pos_x - pos_before_x

        self.collision_y(map, dt, self.vitesse_y)
        self.update_vitesse(dt)

        # Intelligence de saut/escalade : saute si bloqué contre un mur ou si le joueur est plus haut
        if chasing and now >= self.dash_until:
            is_stuck = abs(self.vitesse_x) > 0 and abs(moved_x) < 1.0
            player_above = self.target.pos_y < self.pos_y - 1.5 * self.base_movement

            if (is_stuck or player_above) and self.touch_ground(map):
                if now - getattr(self, "last_ai_jump_time", 0) > 0.8:
                    self.jump(map)
                    self.last_ai_jump_time = now
                    # Si la cible est très haute, on prépare un double saut
                    if self.target.pos_y < self.pos_y - 4.5 * self.base_movement:
                        self.double_jump_pending = True
                        self.double_jump_time = now + 0.25

    def try_dodge(self, map):
        """Toutes les dodge_cooldown secondes, esquive : alterne un dash et un double saut."""

        if self.target is None:
            return

        now = time.perf_counter()
        if now - self.last_dodge < self.dodge_cooldown:
            return
        self.last_dodge = now

        if self.dodge_with_dash:
            #Dash à l'opposé du joueur pour esquiver
            dir = 1 if self.pos_x > self.target.pos_x else -1
            self.dash([dir * self.base_movement * 70, 0])
            self.dash_until = now + 0.35
        else:
            #Double saut : un saut maintenant, le second juste après (voir resolve_double_jump)
            self.jump(map)
            self.double_jump_pending = True
            self.double_jump_time = now + 0.25

        self.dodge_with_dash = not self.dodge_with_dash

    def resolve_double_jump(self, map):
        """Déclenche le 2e saut du double saut une fois le court délai écoulé."""

        if self.double_jump_pending and time.perf_counter() >= self.double_jump_time:
            self.jump(map, force_jump=True)             #force_jump : saute même en l'air
            self.double_jump_pending = False

    def try_spawn_minions(self):
        """Toutes les spawn_cooldown secondes, invoque un squelette et un laseroïde si la limite active n'est pas atteinte."""

        # Filtrer et nettoyer les sbires morts de la liste locale
        self.active_minions = [m for m in self.active_minions if m.is_alive() and not m.dead]

        # Limite dynamique des sbires actifs (2 sbires par joueur, max 8)
        active_limit = min(8, 2 * world.NBR_OF_PLAYER)
        if len(self.active_minions) >= active_limit:
            return

        now = time.perf_counter()
        if now - self.last_spawn < self.spawn_cooldown:
            return
        self.last_spawn = now

        offset = 3 * self.base_movement
        spawn_y = self.pos_y - 2 * self.base_movement

        # Les monstres sont mis dans monsters_to_spawn, que Read_monster enregistre ensuite
        skeleton = Skeleton(self.pos_x + offset, spawn_y)
        laseroide = Laseroide(self.pos_x - offset, spawn_y)

        self.monsters_to_spawn.append(skeleton)
        self.monsters_to_spawn.append(laseroide)

        # Ajouter à notre liste de sbires actifs
        self.active_minions.append(skeleton)
        self.active_minions.append(laseroide)
        self.minions_spawned += 2