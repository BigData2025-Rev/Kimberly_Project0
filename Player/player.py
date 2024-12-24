# create player class
import os
import json
import random
from Util.colors import Colors

DEF_SCALING = 20 # Scaling factor for defense calculation


class Player:
    def __init__(self):
        self.hp = 100.0
        self.attack = 10.0
        self.defense = 0.0
        self.gold = 0
        self.inventory = []
        self.max_hp = 100.0
        self.encounter_count = 1
        self.random_state = random.getstate()

        # Item effects, To be implemented later
        self.critical_chance = 0 # % critical chance
        self.counter = False # if True, player can counter attack
        self.can_AOE = False # if True, player can attack all enemies
        self.dodge_chance = 0 # % chance to dodge an attack


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
        #in red
        print(f'{Colors.RED}You died!{Colors.END}')

    # Calculate damage taken based on player defense and damage reduction
    def takeDamage(self, damage):
        #Formula: Damage Taken = Incoming Damage × (1 / (1 + Defense / Scaling Factor))
        # damage -= self.defense
        damage = damage * (1 / (1 + self.defense / DEF_SCALING))

        if damage < 0:
            damage = 0
        
        self.hp -= damage
        print(f'You take {Colors.RED}{"{0:.2f}".format(damage)}{Colors.END} damage!')
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
        

    # Probably not needed for now
    # def roomReset(self):
    #     self.damage_reduction = 0
    #     self.critical_chance = 0
    #     self.counter = False
    #     self.active_spell = None
    #     self.mana = 100
        
    def printStats(self):
        print(f"{Colors.GREEN}Current Stats:{Colors.END}")
        print(f"HP: {"{0:.2f}".format(self.hp)}/{int(self.max_hp)}, Attack: {"{0:.2f}".format(self.attack)}, Defense: {"{0:.2f}".format(self.defense)}, Gold: {self.gold}")
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
            self.encounter_count = data['encounter_count']
            state = data['random_state']
            random.setstate((state['seed'], tuple(state['state']), state['gauss']))
            return True
        else:
            return False

    def rewardGold(self, gold):
        self.gold += gold
        print(f"{Colors.YELLOW}You have received {gold} gold!{Colors.END}")
        
    #Shop functions to modify stats when purchasing items
    def buyHealthPotion(self, cost: int, percentage: float) -> bool:
        if self.gold >= cost:
            self.gold -= cost
            self.hp += self.max_hp * percentage
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            print(f"{Colors.YELLOW}You have purchased a health potion and now have {"{0:.2f}".format(self.hp)}/{int(self.max_hp)}hp!{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}You do not have enough gold to purchase a health potion!{Colors.END}")
            return False
    
    def buyAttackUpgrade(self, cost) -> bool:
        if self.gold >= cost:
            self.gold -= cost
            self.attack += 3
            print(f"{Colors.YELLOW}Your attack has increased by 3!{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}You do not have enough gold to purchase that item!{Colors.END}")
            return False

    def buyDefenseUpgrade(self, cost) -> bool:
        if self.gold >= cost:
            self.gold -= cost
            self.defense += 2
            print(f"{Colors.YELLOW}Your defense has increased by 2!{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}You do not have enough gold to purchase that item!{Colors.END}")
            return False

    def buyMaxHPUpgrade(self, cost) -> bool:
        if self.gold >= cost:
            self.gold -= cost
            self.max_hp += 25
            self.hp += 25
            print(f"{Colors.YELLOW}Your max HP has increased by 25!{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}You do not have enough gold to purchase that item!{Colors.END}")
            return False


    
    
