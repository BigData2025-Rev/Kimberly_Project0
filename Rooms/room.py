#Abstract room class
from abc import ABC, abstractmethod
from Player.player import Player
from Rooms.boss_room import BossRoom
from Rooms.enemy_room import EnemyRoom
from Rooms.shop_room import ShopRoom
import random as r

class Room(ABC):
    def __init__(self, player):
        self.player = player

    #Method called when player enters the room
    @abstractmethod
    def onEnter(self):
        pass

    #Method called when player exits the room
    @abstractmethod
    def onExit(self):
        pass

    #Method to get options that will be presented to the player
    @abstractmethod
    def getOptions(self):
        pass

    #Returns true if the room is active: enemies still alive, shop still open, etc.
    @abstractmethod
    def isActive(self):
        pass

    #Returns an array of options that the player can take
    #In a combat room, lists the enemies the player can attack
    #In a shop room, lists the items the player can buy
    @abstractmethod
    def getOptions(self):
        pass

    #Static method to generate a new room
    #boss room spawns ever 10 encounters
    #shop spawns in the room before a boss room
    #enemy room spawns otherwise
    @staticmethod
    def getRoom(encounter_count : int):

        if encounter_count % 10 == 0:
            return BossRoom()
        elif encounter_count % 10 == 9:
            return ShopRoom()
        else:
            return EnemyRoom()


