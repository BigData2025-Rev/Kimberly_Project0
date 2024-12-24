from Player.player import Player
from Rooms.room import Room
import json
import random


items = [] # Upgrades and items that can be bought
perks = [] # One time pucahse items
def loadItems():
    global items
    global perks
    with open('GameData/shopItems.json', 'r') as file:
        item_data = json.load(file)
        items = item_data['ShopList']
        perks = item_data['PerkList']

class ShopRoom(Room):
    def __init__(self, encounter_count: int):
        super().__init__(encounter_count)
        self.items_for_sale = []
        self.active = True

    def onEnter(self):
        #pick 3 random items from items, shop can only sell one of each item
        self.items_for_sale = []
        for i in range(3):
            item = random.choice(items)
            while item in self.items_for_sale:
                item = random.choice(items)
            self.items_for_sale.append(item)
        print('You have entered a shop room!')

    def onExit(self, player):
        pass

    def getOptions(self):
        return [self.itemToString(item) for item in self.items_for_sale] + ['Leave']
        #return self.items_for_sale + ['Leave']

    def handleInput(self, action, player : Player):
        if action == len(self.items_for_sale):
            self.active = False
            print('Leaving shop room')
        else:
            item = self.items_for_sale[action]
            item_id = item['name']
            if item_id == 'Big Health Potion':
                success = player.buyHealthPotion(item['cost'], 0.5)
            elif item_id == 'Max Health Upgrade':
                success = player.buyMaxHPUpgrade(item['cost'])
            elif item_id == 'Attack Upgrade':
                success = player.buyAttackUpgrade(item['cost'])
            elif item_id == 'Defense Upgrade':
                success = player.buyDefenseUpgrade(item['cost'])
            elif item_id == 'Small Health Potion':
                success = player.buyHealthPotion(item['cost'], 0.25)
            if success:
                self.items_for_sale.remove(item)

    def itemToString(self, item):
        return f'{item["name"]}: {item["cost"]} gold - {item["description"]}'


    def isActive(self):
        return self.active
