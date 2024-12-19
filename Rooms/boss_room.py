from Rooms.enemy_room import EnemyRoom
from Player.player import Player

class BossRoom(EnemyRoom):
    def __init__(self, encounter_count : int):
        super().__init__(encounter_count)

    def onEnter(self):
        self.enemies = ['Dragon']
        print('You have entered the boss room!')
        print('The boss is a mighty dragon!')

    def onExit(self):
        print("You have defeated the boss!")
        #reward player with gold

    def isActive(self):
        return self.enemies != []

    def attackPlayer(self):
        print('The dragon attacks you!')
        self.player.takeDamage(10)

    def getOptions(self):
        return ['Attack', 'Run']

    def handleInput(self, action):
        if action == 'Attack':
            self.attackPlayer()
        elif action == 'Run':
            print('You run away from the dragon!')
            self.player.roomReset()