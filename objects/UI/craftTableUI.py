from pygameHelper import (
    UI, 
    ImageObject, 
    Vector, 
    Event,
    Manger
)

from objects.UI.itemUI import InventorySlot, ResultSlot

from components.inventory import craft_recipe, is_tools
from components.windowManager import WindowManager

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.UI.InventoryUI import InventoryWindow

class CraftTable(UI):
    def __init__(self, name, tag, visible, position, rotation, parent_name):
        super().__init__(name, 6, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, path="./resource/inventory/craftUI.png", size=(3, 3), follow=True)
        self.components.append(self.image)

        self.window_manager = WindowManager(self, "craft")
        
        self.window_manager.on_open.add_lisner(self.on_open)
        self.window_manager.on_close.add_lisner(self.on_close)

        self.change_recipe = Event()
        self.change_recipe.add_lisner(self.visible_item_result)

        self.on_create_item = Event()

        self.data: list[list[InventorySlot]] = []

        interval = 64
        for i in range(3):
            cache = []
            for j in range(3):

                pos = Vector(j, i) - Vector(1, -1.5)

                pos *= interval

                slot = InventorySlot(name+f"_slot_{j}-{i}", pos, name, "./resource/inventoryItemIcons/itemSlot.png", None, 0)
                slot.is_click.add_lisner(self.change_recipe.invoke)
                slot.right_click.add_lisner(self.change_recipe.invoke)
                self.childrens.append(slot)

                cache.append(slot)
            self.data.append(cache)

        self.result = ResultSlot(name+"_result", [0, 30], name, "./resource/inventoryItemIcons/itemSlot.png", None, 0)
        self.childrens.append(self.result)

    def on_open(self, inventory_ui: 'InventoryWindow'):
        self.location.visible = True

    def on_close(self, inventory_ui: 'InventoryWindow'):
        self.location.visible = False

    def visible_item_result(self):
        item_index, count = self.craft_item()
        if item_index != None:
            self.result.item.set_item_low(item_index, count, is_tools.get(item_index, None))
        else:
            self.result.item.clear()

    def create_item(self):
        item_index, count = self.craft_item()
        recipe = craft_recipe[(item_index, count)]
        for y in range(3):
            for x in range(3):
                if recipe[y][x][0] != None:
                    self.data[y][x].item.sub_item(recipe[y][x][1])
        self.on_create_item.invoke(item_index, count)
        self.visible_item_result()

    def craft_item(self):
        for k, v in craft_recipe.items():
            for i in range(3):
                for j in range(3):
                    if v[i][j][0] != self.data[i][j].item.info.index or v[i][j][1] > self.data[i][j].item.info.count:
                        break
                else:
                    continue
                break
            else:
                return k
        return (None, 0)

    def start(self):
        self.description_object=Manger.scene.get_object("description")
        self.cursor =           Manger.scene.get_object("ItemCursor")
        self.result.setup(self, self.description_object, self.cursor)
        for slots in self.data:
            for slot in slots:
                slot.setup(self.description_object, self.cursor)