from Player.player import Player
from Rooms.enemy_room import EnemyRoom

player = Player()

print('Welcome to the game!')
print('You are a brave adventurer who has been tasked with defeating the evil dragon!')


#Main game loop
while player.isAlive():
    print('You enter a new room!')
    room = EnemyRoom.getRoom(player.encounter_count)
    


#combat loop, used for boss rooms and enemy rooms
def begin_combat(player: Player, room: EnemyRoom):
    room.onEnter()

    while room.isActive():

        print("What would you like to do?")
        print("1. Attack") #Other options later
        action = input("Enter the number of the action you would like to take: ")

        #Player turn
        if action == "1":
            print("You attack the enemy!")
            damage = player.attack()
            print(f'You deal {damage} damage to the enemy!')

        #Enemy turn
        room.attackPlayer()

