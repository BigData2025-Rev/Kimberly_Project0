from Rooms.room import Room
import random as r
from Player.player import Player
from Enemies.enemy import Enemy
from Util.colors import Colors

class EnemyRoom (Room):
    def __init__(self, encounter_count : int):
        super().__init__(encounter_count)
        self.enemies = []

    #Called when player enters the room
    def onEnter(self):
        enemy_count = r.randint(1, 3)
        for i in range(enemy_count):
            self.enemies.append(Enemy(self.encounter_count))
        print(f'You have entered an enemy room! There are {len(self.enemies)} enemies in the room!')
        print(f'The enemies are: {[str(enemy) for enemy in self.enemies]}')

    def onExit(self, player : Player):
        player.rewardGold(8 * len(self.enemies) + 20)
        print(f"{Colors.YELLOW}You have defeated all the enemies!{Colors.END}")

    #Returns a list of all alive enemies in the room
    def getAliveEnemies(self):
        return [enemy for enemy in self.enemies if enemy.hp > 0]

    #Function called on enemy turn to direct enemies to attack
    #Enemy can attack 1 to n times, where n is the number of alive in the room. The same enemy can attack multiple times
    def attackPlayer(self, player : Player):
        
        alive_enemies = self.getAliveEnemies()
        print("Enemy turn!")

        if len(alive_enemies) == 0:
            return
        num_attacks = r.randint(1, len(alive_enemies))
        for i in range(num_attacks):
            alive_enemies = self.getAliveEnemies()
            enemy : Enemy = r.choice(alive_enemies)
            if player.counterStrike():
                print(f"{Colors.GREEN}{enemy.name} attacks and you counter!{Colors.END}")
                dmg = player.attackEnemy(player.counterDamage())
                enemy.takeDamage(dmg)
                continue
            else:
                enemy.attackPlayer(player)


    def getOptions(self):
        return self.enemies
    
    #Checks if there is at least one enemy alive in the room
    def isActive(self):
        for enemy in self.enemies:
            if enemy.hp > 0:
                return True
        return False

