#Abstract room class
from abc import ABC, abstractmethod

import random as r

class Room(ABC):
    def __init__(self, encounter_count : int):
        self.encounter_count = encounter_count
        pass
    #Method called when player enters the room
    @abstractmethod
    def onEnter(self):
        pass

    #Method called when player exits the room
    @abstractmethod
    def onExit(self):
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


