#Inherits from room.py
from Rooms.room import Room
import random as r
from Player.player import Player
from Enemies.enemy import Enemy

class EnemyRoom (Room):
    def __init__(self, encounter_count : int):
        super().__init__(encounter_count)
        self.enemies = [] # list of enemies in the room, max 3

    def onEnter(self):
        #generate a random selection of enemies
        enemy_count = r.randint(1, 3)
        for i in range(enemy_count):
            self.enemies.append(Enemy(self.encounter_count))
        print(f'You have entered an enemy room! There are {len(self.enemies)} enemies in the room!')
        print(f'The enemies are: {[str(enemy) for enemy in self.enemies]}')

    def onExit(self):
        #reward player with gold or items
        pass

    def attackPlayer(self, player : Player):
        print("Enemy turn!")
        #Enemy can attack 1 to n times, where n is the number of alive in the room (1 enemy can attack multiple times)
        num_attacks = r.randint(1, len(self.enemies))
        for i in range(num_attacks):
            enemy : Enemy = r.choice(self.enemies)
            enemy.attackPlayer(player)

    def getOptions(self):
        return self.enemies
    
    #Checks if there is at least one enemy alive in the room
    def isActive(self):
        for enemy in self.enemies:
            if enemy.hp > 0:
                return True
        return False

