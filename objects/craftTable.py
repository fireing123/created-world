from pygameHelper import (
    GameObject, 
    ImageObject, 
    Manger, 
    K_e
)

from components.trigger         import Trigger

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.UI.InventoryUI import InventoryWindow

class CraftTableObject(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, path="./resource/objects/craftTable.png", size=(3, 3))
        self.components.append(self.image)

        self.trigger = Trigger(self, 100, 50, K_e)
        self.trigger.on_interaction.add_lisner(self.open)
        self.components.append(self.trigger)

    def start(self):
        inventory : 'InventoryWindow' = Manger.scene.get_object("inventory")
        self.window = inventory

    def open(self):
        if not self.window.location.parent.visible:
            self.window.open_with('craft')