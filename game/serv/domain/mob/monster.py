from serv.domain.mob.mob import Mob
from serv.config import monster_info
from serv.domain.weapon import weapon1
import math,time

class Monster(Mob):
    def __init__(self, hp, damage, x, y,rad=15, atk_rad=2, atk_speed=1,run_away = -1, id = None,prime = 10,acceleration = 0.2,width = 10,height = 10,knockback_res = 0):

        super().__init__((x,y),hp,id,acceleration=acceleration,height = height,width = width)

        self.hp = hp
        self.damage = damage
        self.resist = False #Resist = ne peut pas subir de dégâts
        #Résistance au knockback : soustraite au knockback reçu. toujours entre [0,3] (0 = aucune résistance)
        self.knockback_res = max(0, min(3, knockback_res))
        self.prime = prime
        
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

    def is_alive(self):
        return self.hp > 0
        
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

    def distance_to_nearest_player(self, lPlayer, map):
        """Distance euclidienne en cases entre le monstre et le joueur."""
        target = None
        best = None
        for p in lPlayer.values():
            if not self.has_line_of_sight(map, p):
                continue
            dx = p.pos_x - self.pos_x
            dy = p.pos_y - self.pos_y
            d = math.hypot(dx, dy)
            if best is None or d < best:
                best = d
                target = p
        if target is None:
            return None, float("inf")
        return target, best / self.base_movement
    
    def dist_to_target_player(self,player):
        """Retourne la distance jusqu'au joueur ciblé"""

        dx = player.pos_x - self.pos_x
        dy = player.pos_y - self.pos_y
        d = math.hypot(dx, dy)
        
        return d/self.base_movement
    # --- Boucle de comportement basique pour tous les monstres ---

    def update(self,map,dt,lPlayer,collision_handler):
        
        if not self.is_alive():
            self.state = "dead"
            return
            
        if self.state == "stunned":
            if time.perf_counter() > getattr(self, 'stun_timer', 0):
                self.state = "idle"
                self.target = None
            else:
                return
        
        if self.target == None : #Choisit la cible, et ne la change que s'il n'a pas de cible
            self.target, self.dist = self.distance_to_nearest_player(lPlayer, map)
        else :
            self.dist = self.dist_to_target_player(self.target) #S'il a déjà une cible, met juste à jour la distance


        #------------degat de collision-----------------#
        if self.dist<self.width/2/self.base_movement and self.collision_damage: 

            if self.collision_start + self.collision_time_reload <= time.perf_counter():
                self.collision_start=time.perf_counter()

                collision_handler.player_take_damage_no_projectile(self.collision_atk,self.target)
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
            if self.dist <= self.attack_radius:
                self.state = "attacking"
            elif self.dist > self.radius * 1.2:
                self.state = "idle"
                self.target = None #Reset de l'aggro

        elif self.state == "run away":
            if self.dist >= self.attack_radius +0 or self.dist < (self.width/2)/self.base_movement : #0 = delta
                self.state = "attacking"


    def take_damage(self, amount,player_did_damage,knockback=0):
        """Retourne True/False selon si le monstre est mort ou non.
        knockback : force du recul (0 = aucun), définie par l'arme ou le sort."""

        if self.dead:
            return False

        if amount!=0 :

            self.life -= amount
            self.send_new_life = True

            #Knockback seulement si l'arme ou le sort en a un, réduit par la résistance du monstre
            effective_kb = max(0, knockback - self.knockback_res)
            if effective_kb and hasattr(player_did_damage, 'pos_x'):
                dx = self.pos_x - player_did_damage.pos_x
                dir = 1 if dx > 0 else -1
                self.vitesse_x = dir * self.base_movement * 15 * effective_kb
                self.vitesse_y = -self.base_movement * 5 * effective_kb
                
            #Étourdi seulement quand le knockback réellement subi dépasse 1.5
            if effective_kb > 1.5:
                self.state = "stunned"
                self.stun_timer = time.perf_counter() + 0.2

            self.focus = False

            if self.life <= 0:
                self.life = 0
                self.die(player_did_damage)

                return True

        return False
    
    def die(self,player_did_damage):

        player_did_damage.update_money(self.prime)

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

    def __init__(self,x,y,id):

        super().__init__(hp=50,damage = 5,x=x,y=y,atk_rad = monster_info.LASEROIDE_ATK_RAD,rad = monster_info.LASEROIDE_RAD,run_away = monster_info.LASEROIDE_TOO_CLOSE,atk_speed = 1,id=id,prime = 15,acceleration = monster_info.LASEROIDE_ACCELERATION,height = 6)

        self.acceleration_y = 20* self.acceleration
        self.knockback_res = 2

        self.name = 1 #Permet d'affihcer le bon monstre
        self.weapon = weapon1.WeaponLaseroide(team = self.team,player = self)

        self.last_time_jump = time.perf_counter()
        self.begin_shot = time.perf_counter()
        self.time_before_shot = 1
        self.angle = 0

    def update(self, map, lPlayer,dt,collision_handler,projectile_manager):

        if self.still_dead():
            return
        
        super().update(map,dt,lPlayer,collision_handler)

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

                if self.angle>90 and self.angle<270 :
                    self.pos_x -= 100
                else :
                    self.pos_x += 100

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
        return
    
    def moving_behavior(self,target,map,dt):
        """Se déplace vers le joueur"""
        if target.pos_x<self.pos_x :
            self.move_left(dt)
        
        else :
            self.move_right(dt)
    
    def leave_behavior(self,target,map,dt):
        """Se déplace à l'opposé du joueur"""
        if target.pos_x<self.pos_x :
            self.move_right(dt)
        
        else :
            self.move_left(dt)

    def attack(self,target,collision_handler,dt,projectile_manager):
        
        infos = self.weapon.trigger_shot(self.angle,(self.pos_x,self.pos_y))

        if infos != None :

            projectiles,events = infos

            for proj in projectiles :

                projectile_manager.add_projectile_create(proj)

        if self.weapon.idx == 0:
            self.focus = False

class Foulli(Monster) :

    def __init__(self,x,y,id):

        super().__init__(hp=10,damage=10,x=x,y=y,atk_rad = monster_info.FOULLI_ATTAQUE_RAD,atk_speed = 1,id=id,prime = 10,acceleration = 0,width = 6,height = 6)

        self.knockback_res = 3

        self.name = 2 #Permet d'afficher le bon monstre / Dans monster all côté client
        self.weapon = weapon1.WeaponLaseroide(team = self.team,player = self)

        self.begin_shot = time.perf_counter()
        self.time_before_shot = 0.3
        self.time_after_shot = 0.5

        self.collision_damage = False

    def update(self, map, lPlayer,dt,collision_handler,projectile_manager):

        if self.still_dead():
            return
        
        super().update(map,dt,lPlayer,collision_handler)

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

                if self.begin_shot+self.time_after_shot <= time.perf_counter() :
                    self.state = "idle"
                    self.focus = False

        elif self.state == "loading" :
            if self.begin_shot+self.time_before_shot <= time.perf_counter() :
                self.state = "attacking"
                self.begin_shot = time.perf_counter()
                if self.dist <=self.attack_radius :
                    self.attack(self.target,collision_handler,dt,projectile_manager)

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

    def attack(self,target,collision_handler,dt,projectile_manager):
        
        damage = self.damage
        collision_handler.player_take_damage_no_projectile(damage,self.target)

class Defendeur(Monster) :

    def __init__(self,x,y,id):

        super().__init__(hp=30,damage =5,x=x,y=y,atk_rad = monster_info.DEFENDEUR_ATK_RAD,rad = monster_info.DEFENDEUR_RAD,run_away = monster_info.DEFENDEUR_TOO_CLOSE,atk_speed = 1,id=id,prime = 10,acceleration = monster_info.DEFENDEUR_ACCELERATION,width = 5,height = 6)

        self.name = 3 #Permet d'afficher le bon monstre / Dans monster all côté client
        self.knockback_res = 3
        #self.weapon = weapon1.WeaponLaseroide(team = self.team,player = self)

        self.begin_attack = time.perf_counter()
        self.time_for_move_to_reach_player = 0.5
        self.len_attack = 2
        self.begin_time_for_attack = time.perf_counter()
        self.time_between_attacks = 0.2

        self.begin_relax = time.perf_counter()
        self.time_to_relax = 2
        self.side = "left" #Côté de l'attaque
        self.hit_box_damage_width = 5
        self.resist = True

        #self.collision_damage = False

    def update(self, map, lPlayer,dt,collision_handler,projectile_manager):

        if self.still_dead():
            return
        
        super().update(map,dt,lPlayer,collision_handler)

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
                        self.move_right(dt)
                    else :
                        self.move_left(dt)

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

                if self.pos_x < self.target.pos_x : #Définit le côté de l'attaque
                    self.side = "right"
                else :
                    self.side = "left"

                self.state = "moving"

            if self.focus :
            
                if self.begin_attack+self.len_attack <= time.perf_counter() : #Signifie arrêter l'attaque

                    self.begin_relax = time.perf_counter()
                    self.resist = False
                    self.state = "idle"

                if self.begin_time_for_attack + self.time_between_attacks < time.perf_counter():

                    self.attack(self.target,collision_handler,dt,projectile_manager)
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
            self.move_left(dt)
        
        else :
            self.move_right(dt)
    
    def leave_behavior(self,target,map,dt):
        """Se déplace vers le joueur"""
        if target.pos_x<self.pos_x :
            self.move_right(dt)
        
        else :
            self.move_left(dt)

    def attack(self,target,collision_handler,dt,projectile_manager):
        """Retourne True si le joueur est bien touché"""
        
        if self.check_if_player_collide_attack(self.target,self.side,self.hit_box_damage_width) :
            damage = self.damage
            collision_handler.player_take_damage_no_projectile(damage,self.target)
            return True
        
        return False

class Escargot(Monster) :

    def __init__(self,x,y,id):

        super().__init__(hp=20,damage =5,x=x,y=y,atk_rad = monster_info.ESCARGOT_ATK_RAD,rad = monster_info.ESCARGOT_RAD,run_away = monster_info.ESCARGOT_TOO_CLOSE,atk_speed = 1,id=id,prime = 10,acceleration = monster_info.ESCARGOT_ACCELERATION,width = 6,height = 6)

        self.knockback_res = 0.5

        self.name = 4 #Permet d'afficher le bon monstre / Dans monster all côté client
        self.direction = "right"

        #self.collision_damage = False

    def update(self, map, lPlayer,dt,collision_handler,projectile_manager):

        if self.still_dead():
            return
        
        super().update(map,dt,lPlayer,collision_handler)

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
    
    def moving_behavior(self,target,map,dt):
        """Se déplace vers le joueur"""

        if self.direction == "right":
            
            delta_y = self.half_height + self.base_movement
            delta_x = self.half_width+self.base_movement
            if self.touch_type(0,delta_x,map,map.dur) : #y puis x
                self.direction = "left"

            elif self.touch_type(delta_y,delta_x,map,map.vide):
                self.direction = "left"
            
            else :
                self.move_right(dt)

        elif self.direction == "left":
            
            delta_y = self.half_height + self.base_movement
            delta_x = -(self.half_width+self.base_movement)
            if self.touch_type(0,delta_x,map,map.dur) : #y puis x
                self.direction = "right"

            elif self.touch_type(delta_y,delta_x,map,map.vide):
                self.direction = "right"
            
            else :
                self.move_left(dt)
    
    def leave_behavior(self,target,map,dt):
        """Se déplace vers le joueur"""

    def attack(self,target,collision_handler,dt,projectile_manager):
        """Retourne True si le joueur est bien touché"""

class Skeleton(Monster):

    def __init__(self, x, y, id):
        super().__init__(hp=20, damage=10, x=x, y=y, rad=30, atk_rad=5, atk_speed=1, id=id,prime = 20)
        
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

    def update(self, map, lPlayer,dt,collision_handler,projectile_manager):

        if self.still_dead():
            return
        
        super().update(map,dt,lPlayer,collision_handler)
       # --- Deplacement selon l'état ---
        if self.state == "idle":
            self.idle_behavior(map,dt)
            
        elif self.state == "moving":
            self.moving_behavior(lPlayer, map,dt)
            
        elif self.state == "attacking":
            self.attack(self.target,collision_handler,dt)
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
        target, _ = self.distance_to_nearest_player(lPlayer, map)

        if target is None:
            return

        dx = target.pos_x - self.pos_x
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
    def attack(self, Player,collision_handler,dt):
       # Inflige des dégâts au joueur en fonction de la vitesse d'attaque
        #for _ in range(self.attack_speed):
        #    Player.take_damage(self.damage)

        #Tim : j'ai juste commente pcq dcp j'ai rajoute le collision handler qui permet de check direct si touche avec 2 rect
        #Et aussi le collision handler envoi au client les degat pour les afficher :)

        damage = int(self.damage*10 * dt) #= inflige self.damage en 1 seconde
        collision_handler.player_take_damage_no_projectile(damage,Player)