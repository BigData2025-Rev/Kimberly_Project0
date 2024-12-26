from Rooms.enemy_room import EnemyRoom
from Enemies.enemy import Enemy
from Player.player import Player
from Util.colors import Colors

class BossRoom(EnemyRoom):
    def __init__(self, encounter_count : int):
        super().__init__(encounter_count)

    def onEnter(self):
        self.enemies.append(Enemy(self.encounter_count))
        print(f'You have entered a boss room!')
        print(f'The boss is: {[str(enemy) for enemy in self.enemies]}')

    def onExit(self, player : Player):
        print(f"{Colors.YELLOW}You have defeated the boss!{Colors.END}")
        player.rewardGold(100)
