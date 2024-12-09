from pygameHelper import (
    GameObject, 
    Physics, 
    ImageObject, 
    SoundSource,
    Manger
)

from components.trigger             import Trigger
from components.inventory           import is_tools

droped_items = []

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.UI.InventoryUI     import InventoryWindow

class DropedItem(GameObject):
    def __init__(self, name, position, item_index, count, durability):
        super().__init__(name, 3, "dropedItem", True, position, 0, "parent")
        self.image = ImageObject(self, value=Manger.tile_sheet['item'].surfaces[item_index], size=(0.5, 0.5))
        self.components.append(self.image)

        self.physics = Physics(self, self.image.rect)
        self.components.append(self.physics)

        self.trigger = Trigger(self, self.image.rect.w+50, self.image.rect.h+50, 2, type=1)
        self.trigger.on_interaction.add_lisner(self.pickup)
        self.components.append(self.trigger)

        self.item_index = item_index
        self.count = count
        self.durability = durability

        self.soundSoruce = SoundSource(self, "./resource/sound/pickup.wav", 0, lambda dist: 0.2)
        self.components.append(self.soundSoruce)

    def start(self):
        self.inventory: 'InventoryWindow' = Manger.scene.get_object("inventory")

    def pickup(self):
        if self.inventory.find_empty_slot() == None:
            slot = self.inventory.get_item(self.item_index)
            if slot == None:
                return
            elif slot.item.info.index in is_tools:
                return
            
        self.inventory.add_item(self.item_index, self.count, self.durability)
        self.soundSoruce.play()
        self.delete()

    def update(self):
        self.rect = self.physics.rect