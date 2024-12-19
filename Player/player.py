# create player class
import os
import json
import random

class Player:
    def __init__(self):
        self.hp = 100.0
        self.attack = 10.0
        self.defense = 0.0
        self.gold = 0
        self.inventory = []
        self.max_hp = 100.0
        self.mana = 100.0
        self.encounter_count = 1
        self.random_state = random.getstate()

        # Spell stats
        self.damage_reduction = 0 # % damage reduction
        self.critical_chance = 0 # % critical chance
        self.counter = False # if True, player will counter attack
        self.active_spell = None # spell that is currently active
        self.mana = 100 # player mana


    # save player data to playerData.json
    def save(self):
        random_state = random.getstate()
        data = {
            'hp': self.hp,
            'attack': self.attack,
            'defense': self.defense,
            'gold': self.gold,
            'inventory': self.inventory,
            'max_hp': self.max_hp,
            'mana': self.mana,
            'encounter_count': self.encounter_count,
            'random_state': {
                'seed': random_state[0],
                'state': list(random_state[1]),
                'gauss': random_state[2]
            }
        }

        with open('GameData/playerData.json', 'w') as file:
            json.dump(data, file)

    #reset player stats
    def reset(self):
        self.hp = 100
        self.attack = 10
        self.defense = 0
        self.gold = 0
        self.inventory = []
        self.save()

    # Calculate damage dealt based on player attack
    def die(self):
        self.save()
        print('You died!')

    # Calculate damage taken based on player defense and damage reduction
    def takeDamage(self, damage):
        damage -= self.defense
        if damage < 0:
            damage = 0
        
        self.hp -= damage
        print(f'You take {damage} damage!')
        if self.hp < 0:
            self.die()

    # Calculate damage dealt based on player attack
    def attackEnemy(self, critical_chance = 0) -> float:
        #pull random number between 0 and 1
        critical = random.random()
        if critical < critical_chance:
            return self.attack * 2
        else:
            return self.attack
        

    # Resets player mana when entering a new room
    def roomReset(self):
        self.damage_reduction = 0
        self.critical_chance = 0
        self.counter = False
        self.active_spell = None
        self.mana = 100
        
    def printStats(self):
        print("Current Stats:")
        print(f"HP: {self.hp}, Attack: {self.attack}, Defense: {self.defense}, Gold: {self.gold}")
        print()

    def isAlive(self):
        return self.hp > 0
    
    # Reset player save data
    def removeSave(self):
        os.remove('GameData/playerData.json')

    #Attempts to load data from playerData.json and stores the data in the player object
    #Returns true if the data was successfully loaded, false otherwise
    def loadData(self) -> bool:
        if os.path.isfile('GameData/playerData.json'):
            with open('GameData/playerData.json', 'r') as file:
                data = json.load(file)
            self.hp = data['hp']
            self.attack = data['attack']
            self.defense = data['defense']
            self.gold = data['gold']
            self.inventory = data['inventory']
            self.max_hp = data['max_hp']
            self.mana = data['mana']
            self.encounter_count = data['encounter_count']
            state = data['random_state']
            random.setstate((state['seed'], tuple(state['state']), state['gauss']))
            return True
        else:
            return False
    
