#Inherits from room.py
from Rooms.room import Room
import random as r
from Player.player import Player

class EnemyRoom (Room):
    def __init__(self):
        self.enemies = [] # list of enemies in the room, max 3

    def onEnter(self):
        #generate a random selection of enemies
        self.enemies = ["Goblin", "Orc", "Troll"]
        print(f'You have entered an enemy room! There are {len(self.enemies)} enemies in the room!')
        print(f'The enemies are: {self.enemies}')

    def onExit(self):
        #reward player with gold or items
        pass

    def attackPlayer(self, player : Player):
        print("Enemy turn!")
        #Enemy can attack 1 to n times, where n is the number of alive in the room (1 enemy can attack multiple times)
        num_attacks = r.randint(1, len(self.enemies))
        for i in range(num_attacks):
            enemy = r.choice(self.enemies)
            print(f'The {enemy} attacks you!')
            #enemy.getDamage() #TODO: Implement enemy class
            #self.player.takeDamage(r.randint(1, 10))

    def getOptions(self):
        return self.enemies
    
    def isActive(self):
        #check if enemies are still alive
        return self.enemies != []

