from Player.player import Player
from Rooms.enemy_room import EnemyRoom
from Rooms.shop_room import ShopRoom
from Rooms.boss_room import BossRoom
import random as r

player = Player()

print('Welcome to the game!')
if player.loadData():
    seed = player.seed
    print('Save file loaded successfully!')
else:
    print('No save file found! Starting new game!')
    seed = input('Enter a seed for the random number generator: ')
    try:
        seed = int(seed)
    except:
        print('Invalid seed, using default seed of 0')
        seed = 0
    #To do: Add add intro

print()
r.seed(seed)
player.seed = seed
player.save()

#Loops through options and returns the index of the selected option
#Error checks for invalid input
def options_prompt(question: str, options: list[str]) -> int:
    selected = -1
    while selected < 0 or selected >= len(options):
        print(question)
        for i in range(len(options)):
            print(f'{i + 1}: {options[i]}')

        try:
            selected = int(input("Enter the number of the action you would like to take: "))-1
        except ValueError:
            print("Invalid input! Please enter a number.")

        if selected < 0 or selected >= len(options):
            print("Invalid input! Please enter a valid number.")
        print()
    return selected


#combat loop, used for boss rooms and enemy rooms
def begin_combat(player: Player, room: EnemyRoom):
    while room.isActive():
        print()
        action = options_prompt("Which enemy would you like to attack?", room.getOptions())

        #Player turn
        if action == 0:
            print("You attack the enemy!")
            damage = player.attackEnemy()
            print(f'You deal {damage} damage to the enemy!')

        print()
        #Enemy turn
        room.attackPlayer(player)

#Shop loop, used for shop rooms
def shop(player: Player, room: ShopRoom):
    while room.isActive():
        print("What would you like to do?")
        print("1. Buy")
        print("2. Leave")
        action = input("Enter the number of the action you would like to take: ")

        if action == "1":
            room.buy()
        elif action == "2":
            print("You leave the shop.")
            player.roomReset()

#Method to generate a new room
def getRoom(encounter_count : int):
    if encounter_count % 10 == 0:
        return BossRoom()
    elif encounter_count % 10 == 9:
        return ShopRoom()
    else:
        return EnemyRoom()

# Called at the end of each room
def end_room() -> bool:
    player.roomReset()
    player.encounter_count += 1
    player.save()
    options_prompt("Do you want to continue?", ["Continue", "Quit"])

#Main game loop
while player.isAlive():
    player.printStats()
    print(f'You enter a new room!')
    room = getRoom(player.encounter_count)
    room.onEnter()

    if isinstance(room, EnemyRoom):
        begin_combat(player, room)
    elif isinstance(room, ShopRoom):
        shop(player, room)

    room.onExit()
    if not end_room():
        break

if not player.isAlive():
    print('Game over! You have died!')
    player.removeSave()
else:
    print("Quitting game!")

