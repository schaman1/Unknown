from serv.domain.mob.mob import Mob
import math

class Monster(Mob):
    def __init__(self, hp, damage, x, y, rad=15, atk_rad=2, atk_speed=1, id = None):

        super().__init__((x,y),hp,id)

        self.hp = hp
        self.damage = damage
        
        self.attack_radius = atk_rad
        self.attack_speed = atk_speed

        self.radius = rad
        
        self.state = "idle"  # idle, moving, attacking, dead

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.life -= amount
        if self.life < 0:
            self.life = 0
        
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

    # --- Boucle de comportement basique pour tous les monstres ---

    def update(self, map,lPlayer):
        
        if not self.is_alive():
            self.state = "dead"
            return

        target, dist = self.distance_to_nearest_player(lPlayer)

        if self.state == "idle":
            if dist <= self.radius:
                self.state = "moving"
       
        elif self.state == "moving":
            if dist <= self.attack_radius:
                self.state = "attacking"
            elif dist > self.radius * 1.2:
                self.state = "idle"
               
        elif self.state == "attacking":
            if dist > self.attack_radius:
               # Revenir à l'état de déplacement si le joueur s'éloigne
                self.state = "moving"
            elif dist <= self.attack_radius:
                # Attaquer le joueur
                 self.attack(target)

    # --- Déplacement pour gestion des collisions ---

    # Vérifie si une cellule est bloquante (dure ou liquide)


    # Essayer de déplacer le monstre selon l'axe X en gérant les collisions


    # Essayer de déplacer le monstre selon l'axe Y en gérant les collisions

    
    # Vérifie si le monstre chevauche une cellule dure


    # Essayer de monter d'une cellule si possible lors d'un déplacement horizontal



#Creation d'un monstre spécifique : le squelette

class Skeleton(Monster):
    def __init__(self, x, y, id):
        super().__init__(hp=50, damage=10, x=x, y=y, rad=30, atk_rad=5, atk_speed=1, id=id)

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

    def update(self, map, lPlayer,dt):
        
        super().update(map,lPlayer)
       # --- Deplacement selon l'état ---
        if self.state == "idle":
            self.idle_behavior(map,dt)
            
        elif self.state == "moving":
            self.moving_behavior(lPlayer, map,dt)
            
        elif self.state == "attacking":
            pass
    
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

        self.gravity_effect()

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

        #print("Here")

        if target is None:
            return

        dx = target.pos_x - self.pos_x
        if abs(dx) < self.base_movement // 10:
            intended_vx = 0
        else:
            intended_vx = self.speed_max if dx > 0 else -self.speed_max

        self.gravity_effect()
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
    def attack(self, lPlayer):
       # Inflige des dégâts au joueur en fonction de la vitesse d'attaque
        for _ in range(self.attack_speed):
            lPlayer.take_damage(self.damage)