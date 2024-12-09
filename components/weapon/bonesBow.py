from pygameHelper import Component, GameObject, TimerTask
from pygameHelper.objects.components.soundSource import SoundSource, SoundManager
from objects.arrow import NomalArrow
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.alotabones import Bones, BowArm

class BonesBow(Component):
    def __init__(self, object, arm) -> None:
        self.object: GameObject = object
        self.arm: BowArm = arm

        self.is_shot = False
        self.shot_wait = TimerTask(1200)

        self.bones: Bones = object

        self.sound_manager = SoundManager({
            "charge_bow": SoundSource(self.object, "./resource/sound/bow/chargeBow.wav", 0, lambda dist: -dist/250 + 0.5),
            "throw_arrow": SoundSource(self.object, "./resource/sound/bow/bowShot.wav", 0, lambda dist: -dist/250 + 0.3)
        })
    
    def update(self):
        if self.is_shot:
            if self.shot_wait.run_periodic_task():
                self.real_shot()
                self.is_shot = False

    def delete(self):
        try:
            self.object.components.remove(self)
        except: pass


    def real_shot(self):
        self.arm.animation_manager.change_animation('idle')
        self.sound_manager.play("throw_arrow")

        arrow_obj = NomalArrow("_bones_arrow", self.bones.layer, 'arrow', True, self.arm.location.world_position, 0, "parent", ignore_tag="notliving")
        arrow_obj.instantiate()
        arrow_obj.setup(self.object)
        arrow_obj.physics.velocity = self.arm.diretion * 30

    def shot(self):
        self.is_shot = True
        self.shot_wait.reset()
        self.arm.animation_manager.change_animation('charge')
        self.sound_manager.play("charge_bow")
