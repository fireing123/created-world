from pygameHelper import Component, GameObject, TimerTask, OnceTimerTask, Rect
from pygameHelper.objects.components.soundSource import SoundSource, SoundManager
from components.hitObject import Attacker
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.zombie import Zombie

class ZombiePunch(Component):
    def __init__(self, object: GameObject) -> None:
        self.object = object

        self.punch_wait = TimerTask(400)
        self.wait = TimerTask(100)
        self.is_wait = True
        self.punch_rect = Rect(0, 0, 45, 15)

        self.attacker = Attacker(self.object, self.punch_rect)
        self.object.components.append(self.attacker)

        self.sound_manager = SoundManager({
            "punch": SoundSource(self.object, "./resource/sound/zombie/middle_kick.wav", 0, lambda dist: 0.3)
        })

        self.zombie: 'Zombie' = object

    def update(self):

        if self.zombie.image.flip[0]:
            self.punch_rect.right = self.object.location.world_position.x
            self.punch_rect.centery = self.object.location.world_position.y
        else:
            self.punch_rect.x = self.object.location.world_position.x
            self.punch_rect.centery = self.object.location.world_position.y

    def delete(self):
        self.attacker.delete()
        try:
            self.object.components.remove(self)
        except: pass

    def punch(self):
        if self.punch_wait.run_periodic_task():
            self.is_wait = True
            self.wait.reset()
            self.zombie.animation_manager.change_animation('punch', True)
            is_hit = self.attacker.hit_check(None, 5, "notliving")
            if is_hit:
                self.sound_manager.play("punch")
