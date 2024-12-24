from Player.player import Player
from Rooms.enemy_room import EnemyRoom
from Rooms.shop_room import ShopRoom
from Rooms.boss_room import BossRoom
from Util.colors import Colors
from Enemies.enemy import load_enemy_data
import random as r

player = Player()

print('Welcome to the game!')
if player.loadData():
    print('Save file loaded successfully!')
else:
    print('No save file found! Starting new game!')
    seed = input('Enter a seed for the random number generator: ')
    try:
        seed = int(seed)
        r.seed(seed)
        player.random_state = r.getstate()
        player.save()

    except:
        print('Invalid seed, using default seed of 0')
        seed = 0
        r.seed(seed)
        player.random_state = r.getstate()
        player.save()

print()
load_enemy_data()


#Loops through options and returns the index of the selected option
#Error checks for invalid input
def options_prompt(question: str, options: list[str]) -> int:
    selected = -1
    while selected < 0 or selected >= len(options):
        print(question)
        for i in range(len(options)):
            #color the number cyan
            print(Colors.CYAN + f'{i + 1}: ' + Colors.END + f'{options[i]}')
            #print(f'{i + 1}: {options[i]}')
        try:
            selected = int(input("Enter your selection: "))-1
        except ValueError:
            print("Invalid input! Please enter a number.")

        if selected < 0 or selected >= len(options):
            print("Invalid input! Please enter a valid number.")
        print()
    return selected


#combat loop, used for boss rooms and enemy rooms
def begin_combat(player: Player, room: EnemyRoom):
    while room.isActive() and player.isAlive():
        action = -1
        while(action == -1):
            print()
            action = options_prompt("Which enemy would you like to attack?", room.getOptions())
            if room.enemies[action].hp <= 0:
                print("That enemy is already defeated. Please select another enemy.")
                action = -1

        #Player turn
        damage = player.attackEnemy()
        print(f'You deal {Colors.RED}{"{0:.2f}".format(damage)}{Colors.END} damage to the enemy!')
        
        room.enemies[action].takeDamage(damage)
        print()


        #Enemy turn
        room.attackPlayer(player)


        print()
        player.printStats()

#Shop loop, used for shop rooms
def shop(player: Player, room: ShopRoom):
    while room.isActive():
        print()
        action = options_prompt("What would you like to purchase?", room.getOptions())
        room.handleInput(action, player)       


#Method to generate a new room
def getRoom(encounter_count : int):
    if encounter_count % 10 == 0:
        return BossRoom(encounter_count)
    elif encounter_count % 10 == 9 or encounter_count % 10 == 3 or encounter_count % 10 == 6:
        return ShopRoom(encounter_count)
    else:
        return EnemyRoom(encounter_count)

# Called at the end of each room
def end_room() -> bool:
    player.roomReset()
    player.encounter_count += 1
    player.save()
    selected = options_prompt("Do you want to continue?", ["Continue", "Quit"])
    return selected == 0

#Main game loop
while player.isAlive():
    print('---------------------------------------------------\n')
    player.printStats()
    print(f"{Colors.BLUE}Room {player.encounter_count}{Colors.END}")
    room = getRoom(player.encounter_count)
    room.onEnter()

    if isinstance(room, EnemyRoom):
        begin_combat(player, room)
        if not player.isAlive():
            break
    elif isinstance(room, ShopRoom):
        shop(player, room)

    room.onExit(player)
    print()
    if not end_room():
        break

if not player.isAlive():
    print('Game over! You have died!')
    player.removeSave()
else:
    print("Quitting game!")

