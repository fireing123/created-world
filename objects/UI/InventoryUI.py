from pygameHelper import (
    UI, 
    ImageObject, 
    Manger, 
    Vector, 
    Event,
    Input, 
    K_e,
    K_ESCAPE
)

from objects.UI.itemUI import InventorySlot

from components.itemInfo import ItemInfo
from components.inventory import is_tools
from components.windowManager import windows, WindowManager

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from objects.player import Player
    from objects.UI.itemUI import CursorItemUI
    from objects.UI.InventoryUI import InventoryWindow

class InventoryWindow(UI):
    def __init__(self, name, position, parent_name, data):
        super().__init__(name, 5, "inventory", True, position, 0, parent_name)
        self.image = ImageObject(self, path="./resource/inventory/window.png", size=(3.3, 3.3), follow=True)
        self.components.append(self.image)

        self.on_add_item = Event()

        self.window_manager = WindowManager(self, "inventory")
        
        self.window_manager.on_open.add_lisner(self.on_open)
        self.window_manager.on_close.add_lisner(self.on_close)

        self.openning_window_type = None

        self.open_this_frame = False

        self.data: List[List[InventorySlot]] = data

        ylen = len(data)
        ycenter = ylen / 2
        xlen = len(data[0])
        xcenter = xlen / 2
        interval = 64
        for i in range(ylen):
            for j in range(xlen):

                pos = Vector(j, i) - Vector(xcenter-0.5, ycenter-0.5)

                pos *= interval

                if i == 0:
                    pos.y -= 32

                pack = data[i][j]
                if pack != None:
                    item_index, count = data[i][j]
                else:
                    item_index = None
                    count = 0

                pos.y += 40

                slot = InventorySlot(name+f"_slot_{j}-{i}", pos, name, "./resource/inventoryItemIcons/itemSlot.png", item_index, count)
                self.childrens.append(slot)

                self.data[i][j] = slot

        self.armor_slot = InventorySlot(name+f"_armor", [-160, -240], name, "./resource/inventoryItemIcons/breastplateSlot.png", None, 0)
        self.childrens.append(self.armor_slot)

        self.boots_slot = InventorySlot(name+f"_boots", [-96, -240], name, "./resource/inventoryItemIcons/bootsSlot.png", None, 0)
        self.childrens.append(self.boots_slot)

    def get_image(self, item_index):
        if item_index != None:
            return Manger.tile_sheet["item"].surfaces[item_index]
        else:
            return None

    def get_item(self, item_index):
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if not self.data[i][j].item.info.is_zero() and self.data[i][j].item.info.index == item_index:
                    return self.data[i][j]
        return None

    def find_empty_slot(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if self.data[i][j].item.info.is_zero():
                    return self.data[i][j]
        return None

    def add_item(self, item_index, count, durability=None):
        item: InventorySlot = self.get_item(item_index)
        if item == None:
            item = self.find_empty_slot()
        elif item.item.info.index in is_tools:
            item = self.find_empty_slot()
        if item == None:
            self.player.droper.drop_item(ItemInfo(item_index, count, durability))
        else:
            self.on_add_item.invoke(item_index, count, durability)
            item.item.add_item_low(item_index, count, durability)

    def sub_item(self, item_index, count):
        item: InventorySlot = self.get_item(item_index)
        item.item.sub_item(count)

    def update(self):
        if not self.open_this_frame:
            if self.player.state != "auto":
                if Input.get_key_down(K_e):
                    if self.player.state == "trigger":
                        self.close()
                    else:
                        self.open_with('inventory')
                else:
                    if Input.get_key_down(K_ESCAPE):
                        if self.player.state == "trigger":
                            self.close()
        else:
            self.open_this_frame = False

    def on_open(self, inventory_ui: 'InventoryWindow'):
        self.location.position = (0, 0)

    def on_close(self, inventory_ui: 'InventoryWindow'):
        self.location.position = (200, 0)

    def open_with(self, with_type):
        self.close()
        self.open_this_frame = True
        self.player.change_animation('trigger', key='idle')
        self.cursor.location.visible = True
        self.location.parent.visible = True

        window = windows[with_type]
        self.openning_window_type = with_type

        window.on_open.invoke(self)

    def close(self):
        self.location.parent.visible = False
        self.player.change_animation('idle')

        if self.openning_window_type != None:
            window = windows[self.openning_window_type]
            window.on_close.invoke(self)
            self.openning_window_type = None

        self.cursor.location.visible = False
        self.description_object.location.visible = False
        obj: 'CursorItemUI' = self.cursor.location.children[0].object

        if not obj.info.is_clean():
            self.add_item(obj.info.index, obj.info.count, obj.info.durability)
            obj.clear()

    def start(self):
        self.player: 'Player' = Manger.scene.get_object("player")
        self.description_object=Manger.scene.get_object("description")
        self.cursor =           Manger.scene.get_object("ItemCursor")
        self.hotbar =           Manger.scene.get_object("hotbar")

        for slots in self.data:
            for slot in slots:
                slot.setup(self.description_object, self.cursor)

        self.armor_slot.setup(self.description_object, self.cursor)
        self.boots_slot.setup(self.description_object, self.cursor)