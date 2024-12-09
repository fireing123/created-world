from pygameHelper import Component, GameObject, TimerTask, Rect
from components.hitObject import Attacker
from components.inventory import ItemIndex
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.player import Player

class Axe(Component):
    def __init__(self, object: GameObject) -> None:
        self.object = object

        self.axe_wait = TimerTask(500)
        self.axe_rect = Rect(0, 0, 40, 20)

        self.attack_check = Attacker(self.object, self.axe_rect)
        self.object.components.append(self.attack_check)

        self.player: Player = object

    def update(self):
        if self.player.state == 'axeEnd':
            if self.axe_wait.not_update_run():
                self.player.change_animation('idle')

    def axe(self):
        if self.axe_wait.run_periodic_task():
            self.player.change_animation('axe', reset=True)
            
    def axe_hit(self):
        if self.player.image.flip[0]:
            self.axe_rect.right = self.object.location.world_position.x
            self.axe_rect.centery = self.object.location.world_position.y
        else:
            self.axe_rect.x = self.object.location.world_position.x
            self.axe_rect.centery = self.object.location.world_position.y
        if self.attack_check.hit_check(ItemIndex.AXE, 10):
            self.player.durability_sub(2)

    def delete(self):
        self.attack_check.delete()
        try:
            self.object.components.remove(self)
        except: pass