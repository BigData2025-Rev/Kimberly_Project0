from Player.player import Player
from Rooms.room import Room

class ShopRoom(Room):
    def __init__(self, encounter_count: int):
        super().__init__(encounter_count)
        self.items = ['Potion', 'Sword', 'Shield', 'Armor']

    def onEnter(self):
        print('You have entered a shop room!')
        print('Items for sale:')
        for item in self.items:
            print(f' - {item}')

    def onExit(self):
        pass

    def getOptions(self):
        return ['Buy', 'Leave']

    def handleInput(self, action):
        if action == 'Buy':
            self.buy()
        elif action == 'Leave':
            print('You leave the shop.')
            self.player.roomReset()

    def buy(self):
        print('What would you like to buy?')
        for item in self.items:
            print(f' - {item}')

        item = input('Enter the name of the item you would like to buy: ')
        if item in self.items:
            if item == 'Potion':
                self.player.buyPotion()
            elif item == 'Sword':
                self.player.buySword()
            elif item == 'Shield':
                self.player.buyShield()
            elif item == 'Armor':
                self.player.buyArmor()
        else:
            print('Invalid item name!')
