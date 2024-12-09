from pygameHelper import Component, GameObject, TimerTask, Rect
from pygameHelper.objects.components.soundSource import SoundSource, SoundManager
from components.inventory import ItemIndex
from components.hitObject import Attacker
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.player import Player

class PickaxeIron(Component):
    def __init__(self, object: GameObject) -> None:
        self.object = object

        self.pickaxe_wait = TimerTask(500)

        self.pickaxe_rect = Rect(0, 0,40, 70)

        self.attacker = Attacker(self.object, self.pickaxe_rect)
        self.object.components.append(self.attacker)

        self.player: 'Player' = object

    def update(self):
        if self.player.state == "pickaxeIron":
            if self.pickaxe_wait.not_update_run():
                self.player.change_animation("idle")

    def delete(self):
        self.attacker.delete()
        try:
            self.object.components.remove(self)
        except: pass


    def pickaxe_iron(self):
        if self.pickaxe_wait.run_periodic_task():
            self.player.change_animation('pickaxeIron', reset=True)
            if self.player.image.flip[0]:
                self.pickaxe_rect.right = self.object.location.world_position.x
                self.pickaxe_rect.centery = self.object.location.world_position.y
            else:
                self.pickaxe_rect.x = self.object.location.world_position.x
                self.pickaxe_rect.centery = self.object.location.world_position.y
            hits = self.attacker.hit_check(ItemIndex.IRON_PICKAXE, 10)
            
            for hit_obj in hits:
                if hit_obj.object.tag in ['stone', 'steel']:
                    self.player.durability_sub(1)

                elif hit_obj.object.tag in ['living', 'notliving', "tree"]:
                    self.player.durability_sub(2)

                