import pygame
from pygameHelper import (
    UI, 
    Rect, 
    Manger, 
    ImageObject
)

from components.inventory import ItemIndex
from components.itemInfo import ItemInfo

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.UI.InventoryUI import InventoryWindow

class HeathBar(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)

    def start(self):
        self.player = Manger.scene.get_object("player")

    def render(self, surface: pygame.Surface, camera):
        cameraed = camera.centerXY(self.render_position)
        pygame.draw.rect(surface, (0, 0, 0), Rect(cameraed.x-5, cameraed.y-5, 150, 20))
        pygame.draw.rect(surface, (255, 51, 51), Rect(cameraed.x, cameraed.y, int(self.player.heath * 1.5), 20))
        
        pygame.draw.rect(surface, (0, 0, 0), Rect(cameraed.x-165, cameraed.y-5, 150, 20))
        pygame.draw.rect(surface, (153, 91, 15), Rect(cameraed.x-160, cameraed.y, int(self.player.hunger * 1.5), 20))

class PlayerArmorState(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, follow=True)
        self.components.append(self.image)

    def start(self):
        self.inventory: 'InventoryWindow' = Manger.scene.get_object("inventory")
        self.inventory.armor_slot.item.on_change_event.add_lisner(self.syss)

    def syss(self, info: ItemInfo):
        if info.index == None:
            self.image.og_image = None
        elif info.index == ItemIndex.BREASTPLATE:
            self.image.og_image = self.get_image(2)
        elif info.index == ItemIndex.WING:
            self.image.og_image = self.get_image(0)

    def get_image(self, item_index):
        if item_index != None:
            return Manger.tile_sheet["mini_item"].surfaces[item_index]
        else:
            return None

class PlayerBootsState(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, follow=True)
        self.components.append(self.image)

    def start(self):
        self.inventory: 'InventoryWindow' = Manger.scene.get_object("inventory")
        self.inventory.boots_slot.item.on_change_event.add_lisner(self.syss)

    def syss(self, info: ItemInfo):
        if info.index == None:
            self.image.og_image = None
        elif info.index == ItemIndex.BOOTS:
            self.image.og_image = self.get_image(1)

    def get_image(self, item_index):
        if item_index != None:
            return Manger.tile_sheet["mini_item"].surfaces[item_index]
        else:
            return None