# create player class
import os
import json
import random
from Util.colors import Colors

DEF_SCALING = 20 # Scaling factor for defense calculation

#Factors for perks
REGEN = 0.05
COUNTER_DMG = 1.5
COUNTER_CHANCE = 0.1
CRIT_CHANCE = 0.2
AOE_DMG = 0.4
DODGE_CHANCE = 0.1

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
        self.perks = {
            'critical_chance': False,
            'counter': False,
            'can_AOE': False,
            'dodge_chance': False,
            'regen': False
        }


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
            },
            'perks':{
                'critical_chance': self.perks['critical_chance'],
                'counter': self.perks['counter'],
                'can_AOE': self.perks['can_AOE'],
                'dodge_chance': self.perks['dodge_chance'],
                'regen': self.perks['regen']
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

    # Called at the beginning of each room
    def startRoom(self):
        if self.perks['regen']:
            regen_amount = self.max_hp * REGEN
            self.hp += regen_amount
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            print(f"{Colors.GREEN}+{regen_amount}HP{Colors.END}")

    # Calculate damage dealt based on player attack
    def die(self):
        self.save()
        print(f'{Colors.RED}You died!{Colors.END}')

    # Calculate damage taken based on player defense
    def takeDamage(self, damage):
        dodge_chance = 0
        if self.perks['dodge_chance']:
            dodge_chance = DODGE_CHANCE

        if random.random() < dodge_chance:
            print(f"{Colors.GREEN}You dodged the attack!{Colors.END}")
            return
        damage = damage * (1 / (1 + self.defense / DEF_SCALING))

        if damage < 0:
            damage = 0
        self.hp -= damage
        print(f'You take {Colors.RED}{"{0:.2f}".format(damage)}{Colors.END} damage!')
        if self.hp < 0:
            self.die()

    #If the player has bought the counter perk, they have a chance to counter attack when attacked
    def counterStrike(self) -> bool:
        if self.perks['counter']:
            if random.random() < COUNTER_CHANCE:
                return True
        return False
    
    #Returns the damage dealt by a counter attack, if the player has the counter perk
    def counterDamage(self):
        if self.perks['counter']:
            return COUNTER_DMG
        else:
            return 0
    
    #Returns the damage dealt by an AOE attack, if the player has the AOE perk
    def aoeDamage(self):
        if self.perks['can_AOE']:
            return AOE_DMG
        else:
            return 0



    # Calculate damage dealt based on player attack
    def attackEnemy(self, multiplier = 1) -> float:
        if self.perks['critical_chance']:
            critical_chance = CRIT_CHANCE
        else:
            critical_chance = 0
        
        if random.random() < critical_chance:
            print(f"{Colors.RED}Critical hit!{Colors.END}")
            damage = self.attack * 2 * multiplier
        else:
            damage = self.attack * multiplier

        print(f'You deal {Colors.RED}{"{0:.2f}".format(damage)}{Colors.END} damage to the enemy!')
        return damage
        
        
    def printStats(self):
        print(f"{Colors.MAGENTA}Current Stats:{Colors.END}")
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
            self.perks = data['perks']
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

    #Perk functions to modify player stats and abilities
    def buyCriticalChance(self, cost) -> bool:
        if self.gold >= cost:
            self.gold -= cost
            self.perks['critical_chance'] = True
            print(f"{Colors.YELLOW}You now have a 20% chance for critical hits!{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}You do not have enough gold to purchase that item!{Colors.END}")
            return False

    def buyCounter(self, cost) -> bool:
        if self.gold >= cost:
            self.gold -= cost
            self.perks['counter'] = True
            print(f"{Colors.YELLOW}When attacked, you now have a 10% chance to counter attack!{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}You do not have enough gold to purchase that item!{Colors.END}")
            return False
        
    def buyAOE(self, cost) -> bool:
        if self.gold >= cost:
            self.gold -= cost
            self.perks['can_AOE'] = True
            print(f"{Colors.YELLOW}Dealing damage will now do 40% damage to all enemies in a room!{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}You do not have enough gold to purchase that item!{Colors.END}")
            return False
        
    def buyDodgeChance(self, cost) -> bool:
        if self.gold >= cost:
            self.gold -= cost
            self.perks['dodge_chance'] = True
            print(f"{Colors.YELLOW}You now have a 10% chance to dodge an attack!{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}You do not have enough gold to purchase that item!{Colors.END}")
            return False
    
    def buyHealthRegen(self, cost) -> bool:
        if self.gold >= cost:
            self.gold -= cost
            self.perks['regen'] = True
            print(f"{Colors.YELLOW}You now regenerate 5% HP per turn!{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}You do not have enough gold to purchase that item!{Colors.END}")
            return False

    
    
