from pygameHelper import Component, GameObject, TimerTask, Rect
from pygameHelper.objects.components.soundSource import SoundSource, SoundManager
from components.inventory import ItemIndex
from components.hitObject import Attacker
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from objects.player import Player

class Sword(Component):
    def __init__(self, object: GameObject) -> None:
        self.object = object

        self.sword_index = 0

        self.sword_min_wait = TimerTask(300)
        self.sword_wait = TimerTask(500)

        self.sword1_rect = Rect(0, 0, 50, 50)
        self.sword2_rect = Rect(0, 0, 60, 100)

        self.attacker = Attacker(self.object, self.sword1_rect)
        self.object.components.append(self.attacker)

        self.sound_manager = SoundManager({
            "sword1": SoundSource(self.object, "./resource/sound/sword/swing1.wav", 0, lambda dist: 0.3),
            "sword2": SoundSource(self.object, "./resource/sound/sword/swing2.wav", 0, lambda dist: 0.3)
        })
        self.object.components.append(self.sound_manager)

        self.player: 'Player' = object

    def update(self):
        if self.player.state in ['sword1', 'sword2']:
            if self.sword_wait.not_update_run():
                self.sword_wait.last_update = 0
                self.sword_index = 0
                self.player.change_animation('idle')

    def sword(self):
        if self.sword_wait.run_periodic_task():
            self.sword_index = 0
            self.swing(self.sword_index)
            self.sword_min_wait.reset()
        elif self.sword_min_wait.run_periodic_task():
            self.sword_wait.reset()
            self.sword_index += 1
            if self.sword_index == 2:
                self.sword_index = 0
            self.swing(self.sword_index)

    def swing(self, index):
        if index == 0:
            self.sound_manager.play("sword1")
            self.player.change_animation('sword1', reset=True)
            if self.player.image.flip[0]:
                self.object.location.position.x -= 4
                self.sword1_rect.right = self.object.location.world_position.x
                self.sword1_rect.centery = self.object.location.world_position.y
            else:
                self.object.location.position.x += 4
                self.sword1_rect.x = self.object.location.world_position.x
                self.sword1_rect.centery = self.object.location.world_position.y
            self.attacker.rect = self.sword1_rect
            hits = self.attacker.hit_check(ItemIndex.SWORD, 10)
            
        else:
            self.sound_manager.play("sword2")
            self.player.change_animation('sword2', reset=True)
            if self.player.image.flip[0]:
                self.object.location.position.x -= 9
                self.sword2_rect.right = self.object.location.world_position.x
                self.sword2_rect.centery = self.object.location.world_position.y
            else:
                self.object.location.position.x += 9
                self.sword2_rect.x = self.object.location.world_position.x
                self.sword2_rect.centery = self.object.location.world_position.y
            self.attacker.rect = self.sword2_rect
            hits = self.attacker.hit_check(ItemIndex.SWORD, 15)

        for hit_object in hits:
            if hit_object.object.tag in ['living', 'notliving']:
                self.player.durability_sub(1)