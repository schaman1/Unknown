from serv.domain.mob.mob import Mob
from serv.config import monster_info
from serv.domain.weapon import weapon1
import math,time

class Monster(Mob):
    def __init__(self, hp, damage, x, y,rad=15, atk_rad=2, atk_speed=1,run_away = -1, id = None,prime = 10,acceleration = 0.2):

        super().__init__((x,y),hp,id,acceleration=acceleration,height = 6)

        self.hp = hp
        self.damage = damage
        self.prime = prime
        
        self.attack_radius = atk_rad
        self.attack_speed = atk_speed
        self.run_away_rad = run_away

        self.radius = rad

        self.target = None #Set the target to None
        
        self.state = "idle"  # idle, moving, attacking, dead

    def is_alive(self):
        return self.hp > 0
        
    def distance_to_nearest_player(self, lPlayer):
        """Distance euclidienne en cases entre le monstre et le joueur."""
        target = None
        best = None
        for p in lPlayer.values():
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
        """Return dis to target player"""

        dx = player.pos_x - self.pos_x
        dy = player.pos_y - self.pos_y
        d = math.hypot(dx, dy)
        
        return d/self.base_movement
    # --- Boucle de comportement basique pour tous les monstres ---

    def update(self,map,dt,lPlayer,collision_handler):
        
        if not self.is_alive():
            self.state = "dead"
            return
        
        if self.target == None : #Set the target and change only if has no target
            self.target, dist = self.distance_to_nearest_player(lPlayer)
        else :
            dist = self.dist_to_target_player(self.target) #If already has a target, just update the dist

        if self.state == "idle":
            if dist <= self.radius:
                self.state = "moving"
       
        elif self.state == "attacking":
            if dist > self.attack_radius:
               # Revenir à l'état de déplacement si le joueur s'éloigne
                self.state = "moving"
            elif dist <= self.run_away_rad:
                # Fui car ennemy trop proche. Si pas cette up, jamais declenché
                self.state = "run away"

        elif self.state == "moving":
            if dist <= self.attack_radius:
                self.state = "attacking"
            elif dist > self.radius * 1.2:
                self.state = "idle"
                self.target = None #Reset de l'aggro

        elif self.state == "run away":
            if dist >= self.attack_radius +0 : #0 = delta
                self.state = "attacking"

    def take_damage(self, amount,player_did_damage):
        """Return True/False if is dead or not"""

        if self.dead:
            return False

        if amount!=0 :

            self.life -= amount
            self.send_new_life = True

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
        self.full_heal()

    def get_angle(self,player):

        adjacent = player.pos_x-self.pos_x

        opp = (player.pos_y + player.height//2)-self.pos_y

        hyp = math.sqrt(opp**2+adjacent**2)
        angle = math.acos(adjacent/hyp)

        angle = angle*180/math.pi #Convert to deg

        return int(angle)

    # --- Déplacement pour gestion des collisions ---

    # Vérifie si une cellule est bloquante (dure ou liquide)


    # Essayer de déplacer le monstre selon l'axe X en gérant les collisions


    # Essayer de déplacer le monstre selon l'axe Y en gérant les collisions

    
    # Vérifie si le monstre chevauche une cellule dure


    # Essayer de monter d'une cellule si possible lors d'un déplacement horizontal



#Creation d'un monstre spécifique : le squelette

class Laseroide(Monster) :

    def __init__(self,x,y,id):

        super().__init__(hp=50,damage = 5,x=x,y=y,atk_rad = monster_info.LASEROIDE_ATK_RAD,rad = monster_info.LASEROIDE_RAD,run_away = monster_info.LASEROIDE_TOO_CLOSE,atk_speed = 1,id=id,prime = 15,acceleration = monster_info.LASEROIDE_ACCELERATION)

        self.acceleration_y = 20* self.acceleration

        self.name = 1 #Permet d'affihcer le bon monstre
        self.weapon = weapon1.WeaponLaseroide(team = self.team,player = self)

        self.last_time_jump = time.perf_counter()

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
            self.attack(self.target,collision_handler,dt,projectile_manager)

        delta = self.move_all(map,dt,collision_handler)

        self.check_if_jump(delta,map)

    def check_if_jump(self,delta,map):

        if delta[0]==0 and (self.state == "run away" or self.state=="moving") and self.last_time_jump+1 < time.perf_counter():
            if self.jump(map): #if succesfull
                self.last_time_jump = time.perf_counter()

        elif delta[1]>0 and self.last_time_jump+1 < time.perf_counter() :
            if self.jump(map): #if succesfull
                self.last_time_jump = time.perf_counter()

        elif delta[0]!=0:
            self.last_time_jump = time.perf_counter()


    def idle_behavior(self,map,dt):
        """Stay in his spot"""
        return
    
    def moving_behavior(self,target,map,dt):
        """Move to the player"""
        if target.pos_x<self.pos_x :
            self.move_left(dt)
        
        else :
            self.move_right(dt)
    
    def leave_behavior(self,target,map,dt):
        """Move to the player"""
        if target.pos_x<self.pos_x :
            self.move_right(dt)
        
        else :
            self.move_left(dt)

    def attack(self,target,collision_handler,dt,projectile_manager):

        angle = self.get_angle(self.target)
        
        infos = self.weapon.trigger_shot(angle,(self.pos_x,self.pos_y))

        if infos != None :

            projectiles,events = infos

            for proj in projectiles :

                projectile_manager.add_projectile_create(proj)


class Skeleton(Monster):

    def __init__(self, x, y, id):
        super().__init__(hp=20, damage=10, x=x, y=y, rad=30, atk_rad=5, atk_speed=1, id=id,prime = 20)

        self.name = 0
        
        #idle state preset, peux chnanger selon le monstre
        self.direction = 1
        self.idle_min_x = x - 30 *self.base_movement
        self.idle_max_x = x + 30 *self.base_movement
        
        #diffent speed selon l'etat
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
        target, _ = self.distance_to_nearest_player(lPlayer)

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