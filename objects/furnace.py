from pygameHelper import (
    GameObject, 
    ImageObject, 
    Animation,
    AnimationManager,
    Manger, 
    K_e
)

from components.trigger import Trigger
from components.inventory import is_fuel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.UI.furnaceUI import Furnace

class FurnaceObject(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self)
        self.components.append(self.image)

        idle_animation = Animation(float('inf'),    self.image, sheet="furnace")
        fire_aniamtion = Animation(200,             self.image, sheet="furnaceFire")

        idle_animation.change_image()

        self.animation_manager = AnimationManager(self, {
            "idle": idle_animation,
            "fire": fire_aniamtion
        }, "idle")

        self.components.append(self.animation_manager)

        self.trigger = Trigger(self, 100, 50, K_e)
        self.trigger.on_interaction.add_lisner(self.open)
        self.components.append(self.trigger)

    def start(self):
        self.window = Manger.scene.get_object("inventory")
        self.furnace_ui: 'Furnace' = Manger.scene.get_object("furnace")

    def update(self):
        if self.furnace_ui.fire_power == 0:
            if self.furnace_ui.is_can_fire() and self.furnace_ui.fuel_slot.item.info.index in is_fuel:
                self.animation_manager.change_animation("fire")
            else:
                self.animation_manager.change_animation("idle")
        else:
            self.animation_manager.change_animation("fire")

    def open(self):
        if not self.window.location.parent.visible:
            self.window.open_with('furnace')