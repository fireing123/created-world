from pygameHelper import (
    GameObject, 
    ImageObject, 
    K_e, 
    Manger
)

from components.trigger import Trigger

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.UI.InventoryUI import InventoryWindow

class BossCaller(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, path="./resource/boss/bosscallor.png", size=(3, 3))
        self.components.append(self.image)

        self.trigger = Trigger(self, 100, 100, K_e)
        self.trigger.on_interaction.add_lisner(self.open)
        self.components.append(self.trigger)

    def start(self):
        self.inventory : 'InventoryWindow' = Manger.scene.get_object("inventory")
        
        self.real_boss = Manger.scene.get_object("realboss")
        self.fake_boss = Manger.scene.get_object("fakeboss")

    def open(self):
        if self.real_boss.location.world_visible or self.fake_boss.location.world_visible:
            ...
        else:
            if not self.inventory.location.parent.visible:
                self.inventory.open_with('altar')