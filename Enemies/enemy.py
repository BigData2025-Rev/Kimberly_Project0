import json
import random as r

class Enemy():
    #Pulls a random enemy from the enemyList.json file
    def __init__(self, encounter_count : int):
        with open('GameData/enemyList.json', 'r') as file:
            data = json.load(file)
            rand_enemy = data[r.randint(0, 3)] #later change to be based on encounter_count
            self.name = rand_enemy['name']
            self.hp = rand_enemy['hp']
            self.attack = rand_enemy['attack']

        #To do: Implement scaling based on encounter_count

    #Override to string method
    def __str__(self):
        if(self.hp <= 0):
            return f"Enemy Defeated"
        return f"{self.name}: {self.hp} HP, {self.attack} Attack"
    
    def takeDamage(self, damage) -> bool:
        self.hp -= damage
        if self.hp <= 0:
            self.die()
            self.hp = 0

    def attackPlayer(self, player):
        print(f'The {self.name} attacks you')
        player.takeDamage(self.attack)

    def die(self):
        print(f'The {self.name} has died!')