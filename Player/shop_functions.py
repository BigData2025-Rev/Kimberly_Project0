from Util.colors import Colors
from Player.player import Player

def printShopMessage(gold_remaining : int, cost : int, message : str):
    print(f"{Colors.RED}-{cost} gold{Colors.END}")
    print(f"{Colors.YELLOW}{message}{Colors.END}")
    print(f"{Colors.YELLOW}Gold remaining: {gold_remaining}{Colors.END}")

def printFailMessage():
    print(f"{Colors.RED}You do not have enough gold to purchase that item!{Colors.END}")

#Shop functions to modify stats when purchasing items
def buyHealthPotion(player : Player, cost: int, percentage: float) -> bool:
    if player.gold >= cost:
        player.gold -= cost
        player.hp += player.max_hp * percentage
        if player.hp > player.max_hp:
            player.hp = player.max_hp
        printShopMessage(player.gold, cost, f"You have purchased a health potion and now have {"{0:.2f}".format(player.hp)}/{int(player.max_hp)}hp!")
        return True
    else:
        printFailMessage()        
        return False

def buyAttackUpgrade(player : Player, cost : int) -> bool:
    if player.gold >= cost:
        player.gold -= cost
        player.attack += 3
        printShopMessage(player.gold, cost, "Your attack has increased by 3!")
        return True
    else:
        printFailMessage()
        return False

def buyDefenseUpgrade(player : Player, cost : int) -> bool:
    if player.gold >= cost:
        player.gold -= cost
        player.defense += 2
        printShopMessage(player.gold, cost, "Your defense has increased by 2!")
        return True
    else:
        printFailMessage()
        return False

def buyMaxHPUpgrade(player : Player, cost : int) -> bool:
    if player.gold >= cost:
        player.gold -= cost
        player.max_hp += 25
        player.hp += 25
        printShopMessage(player.gold, cost, "Your max HP has increased by 25!")
        return True
    else:
        printFailMessage()
        return False

#Perk functions to modify player stats and abilities
def buyCriticalChance(player : Player, cost : int) -> bool:
    if player.gold >= cost:
        player.gold -= cost
        player.perks['critical_chance'] = True
        printShopMessage(player.gold, cost, f"You now have a 30% chance for critical hits!")
        return True
    else:
        printFailMessage()
        return False

def buyCounter(player : Player, cost : int) -> bool:
    if player.gold >= cost:
        player.gold -= cost
        player.perks['counter'] = True
        printShopMessage(player.gold, cost, f"When attacked, you now have a 10% chance to counter attack!")
        return True
    else:
        printFailMessage()
        return False
    
def buyAOE(player : Player, cost : int) -> bool:
    if player.gold >= cost:
        player.gold -= cost
        player.perks['can_AOE'] = True
        printShopMessage(player.gold, cost, f"Dealing damage will now do 40% damage to all enemies in a room!")
        return True
    else:
        printFailMessage()
        return False
    
def buyDodgeChance(player : Player, cost : int) -> bool:
    if player.gold >= cost:
        player.gold -= cost
        player.perks['dodge_chance'] = True
        printShopMessage(player.gold, cost, f"You now have a 20% chance to dodge an attack!")
        return True
    else:
        printFailMessage()
        return False

def buyHealthRegen(player : Player, cost : int) -> bool:
    if player.gold >= cost:
        player.gold -= cost
        player.perks['regen'] = True
        printShopMessage(player.gold, cost, f"You now regenerate 5% HP when you enter a room!")
        return True
    else:
        printFailMessage()
        return False