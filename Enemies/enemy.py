import json
import random as r
from Util.colors import Colors

enemy_list = []
boss_list = []

def load_enemy_data():
    global enemy_list
    global boss_list
    with open('GameData/enemyList.json', 'r') as file:
        enemy_list = json.load(file)

    with open('GameData/bossList.json', 'r') as file:
        boss_list = json.load(file)


class Enemy():
    #Pulls a random enemy from the enemyList.json file
    def __init__(self, encounter_count : int):
        if encounter_count % 10 == 0:
            enemy_data = boss_list[(encounter_count // 10) - 1]
        else:
            diff = encounter_count // 10
            enemy_data = enemy_list[r.randint(diff, diff+2)] #later change to be based on encounter_count
        
        self.name = enemy_data['name']
        self.hp = enemy_data['hp']
        self.attack = enemy_data['attack']

    #Override to string method
    def __str__(self):
        if(self.hp <= 0):
            return f"Enemy Defeated"
        return f"{self.name}: {"{0:.2f}".format(self.hp)} HP, {"{0:.2f}".format(self.attack)} Attack"
    
    def takeDamage(self, damage) -> bool:
        self.hp -= damage
        if self.hp <= 0:
            self.die()
            self.hp = 0

    def attackPlayer(self, player):
        print(f'The {self.name} attacks you')
        player.takeDamage(self.attack)

    def die(self):
        print(f'{Colors.YELLOW}The {self.name} has died!{Colors.END}')
