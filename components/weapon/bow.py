from pygameHelper import Component, GameObject, TimerTask, Rect
from pygameHelper.objects.components.soundSource import SoundSource, SoundManager
from objects.arrow import NomalArrow
from components.inventory import ItemIndex
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.player import Player, BowArm

class Bow(Component):
    def __init__(self, object, arm) -> None:
        self.object: GameObject = object
        self.arm: BowArm = arm

        self.bow_charge_power = 0
        self.bow_can = False

        self.player: Player = object

        self.sound_manager = SoundManager({
            "charge_bow": SoundSource(self.object, "./resource/sound/bow/chargeBow.wav", 0, lambda dist: 0.5),
            "ready_bow": SoundSource(self.object, "./resource/sound/bow/readyBow/reflection.wav", 0, lambda dist: 0.3),
            "throw_arrow": SoundSource(self.object, "./resource/sound/bow/bowShot.wav", 0, lambda dist: 0.3)
        })
    
    def update(self):
        item_index = self.player.hotbar.get_focuse_slot().item.info.index
            
        if self.arm.location.visible != (item_index == ItemIndex.BOW):
            self.arm.location.visible = item_index == ItemIndex.BOW
            self.bow_charge_power = 0
            self.arm.animation_manager.change_animation('idle')
            self.sound_manager.stop('charge_bow')

    def delete(self):
        try:
            self.object.components.remove(self)
        except: pass

    def ready(self):
        self.bow_charge_power = 0
        if self.player.inventory.get_item(ItemIndex.ARROW) != None:
            self.arm.animation_manager.change_animation('charge')
            self.sound_manager.play("charge_bow")
            self.bow_can = True
        else:
            self.bow_can = False

    def charge(self):
        if self.bow_can:
            if self.bow_charge_power == 60:
                self.sound_manager.play("ready_bow")
            if self.bow_charge_power <= 60:
                self.bow_charge_power += 1

    def shot(self):
        if self.bow_can:
            self.arm.animation_manager.change_animation('idle')
            self.sound_manager.stop('charge_bow')
            if self.bow_charge_power <= 20:
                return
            self.sound_manager.play("throw_arrow")
            arrow = self.player.inventory.get_item(ItemIndex.ARROW)
            if arrow != None:
                self.player.durability_sub(1)
                arrow.item.sub_item(1)
                arrow_obj = NomalArrow("player_arrow", self.player.layer, 'arrow', True, self.arm.location.world_position, 0, "parent")
                arrow_obj.instantiate()
                arrow_obj.setup(self.object)
                arrow_obj.physics.velocity = self.arm.diretion * (self.bow_charge_power / 3)