class mobs:
    def __init__(self, hp, damage):
        self.hp = hp
        self.damage = damage

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0