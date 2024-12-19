class Enemy():
    def __init__(self):
        #To do: Pull data from json file to determine name, hp, and attack
        self.hp = 10.0
        self.attack = 5.0
        self.name = 'Goblin'
    
    def takeDamage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.die()
            self.hp = 0

    def die(self):
        print(f'The {self.name} has died!')