from pygameHelper import Component, GameObject, TimerTask, Rect
from pygameHelper.objects.components.soundSource import SoundSource, SoundManager
from components.hitObject import Attacker
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.player import Player

class Punch(Component):
    def __init__(self, object: GameObject) -> None:
        self.object = object

        self.punch_index = 0

        self.punch_min_wait = TimerTask(200)
        self.punch_wait = TimerTask(400)

        self.punch_rect = Rect(0, 0, 30, 15)
        self.punch_second_rect = Rect(0, 0, 40, 15)

        self.attacker = Attacker(self.object, self.punch_rect)
        self.object.components.append(self.attacker)

        self.sound_manager = SoundManager({
            "punch": SoundSource(self.object, "./resource/sound/punch/first.wav", 0, lambda dist: 0.1),
            "punch_second": SoundSource(self.object, "./resource/sound/punch/second.wav", 0, lambda dist: 0.1),
            "punch_fail": SoundSource(self.object, "./resource/sound/punch/fail.wav", 0, lambda dist: 0.5)
        })

        self.player: 'Player' = object

    def update(self):
        if self.player.state in ['punch1', 'punch2']:
            if self.punch_wait.not_update_run():
                self.punch_wait.last_update = 0
                self.punch_index = 0
                self.player.change_animation('idle')

    def delete(self):
        self.attacker.delete()
        try:
            self.object.components.remove(self)
        except: pass


    def punch(self):
        if self.punch_wait.run_periodic_task():
            self.punch_index = 0
            self.step(self.punch_index)

        elif self.punch_min_wait.run_periodic_task():
            self.punch_index += 1   
            if self.punch_index == 2:
                self.punch_index = 0
            self.step(self.punch_index)
        self.punch_wait.reset()

    def step(self, index):
        if index == 0:
            if self.player.image.flip[0]:
                self.object.location.position.x -= 7
                self.punch_rect.right = self.object.location.world_position.x
                self.punch_rect.centery = self.object.location.world_position.y
            else:
                self.object.location.position.x += 7
                self.punch_rect.x = self.object.location.world_position.x
                self.punch_rect.centery = self.object.location.world_position.y
            self.attacker.rect = self.punch_rect
            is_hit = self.attacker.hit_check(None, 5)
            if is_hit:
                self.sound_manager.play("punch")
            else:
                self.sound_manager.play("punch_fail")
            self.player.change_animation('punch1')
        else:
            if self.player.image.flip[0]:
                self.object.location.position.x -= 9
                self.punch_second_rect.right = self.object.location.world_position.x
                self.punch_second_rect.centery = self.object.location.world_position.y
            else:
                self.object.location.position.x += 9
                self.punch_second_rect.x = self.object.location.world_position.x
                self.punch_second_rect.centery = self.object.location.world_position.y
            self.attacker.rect = self.punch_second_rect
            is_hit = self.attacker.hit_check(None, 7)
            if is_hit:
                self.sound_manager.play("punch_second")
            else:
                self.sound_manager.play("punch_fail")
            self.player.change_animation('punch2')