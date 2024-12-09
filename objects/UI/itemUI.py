import pygame
from pygameHelper import *

from objects.UI.ItemCursor  import ItemCursor

from components.inventory   import is_tools
from components.itemInfo    import ItemInfo

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.UI.itemDescriptionUI   import ItemDescription
    from objects.UI.InventoryUI         import InventoryWindow

class InventorySlot(Button):
    def __init__(self, name, position, parent_name, default, item_index, count):
        super().__init__(name, 6, "slot", True, position, 0, parent_name, default, size=(3, 3))

        self.is_click.add_lisner(self.slot_click)
        self.right_click  = Event()
        image = self.get_image(item_index)
        self.item = ItemUI(name+"_item", 7, [0, 0], name, image, item_index, count)
        self.childrens.append(self.item)

        self.is_click.add_lisner(self.on_change_event)
        self.right_click.add_lisner(self.on_change_event)

    def on_change_event(self):
        if self.item.info.is_clean():
            self.description_object.location.visible = False
        else:
            self.description_object.show_description.reset()
            if self.description_object.location.visible:
                self.description_object.set_item(self.item.info.index)

    def get_image(self, item_index):
        if item_index != None:
            return Manger.tile_sheet["item"].surfaces[item_index]
        else:
            return None

    def on_mouse_enter(self, pos: tuple[int, int]):
        self.description_object.show_description.reset()

    def on_mouse_stay(self, pos: tuple[int, int]):
        if Input.get_mouse_down(2):
            cursor_item : ItemUI = self.cursor.location.children[0].object
            cursor_info: ItemInfo = cursor_item.info
            slot_item = self.item

            if pygame.key.get_mods() & pygame.KMOD_SHIFT and not slot_item.info.is_clean():
                info = self.item.extract_item(self.item.info.count)
                self.inventory.add_item(info.index, info.count, info.durability)
            else:
                if not cursor_info.is_clean():
                    if cursor_info.index == slot_item.info.index or slot_item.info.index == None:
                        if cursor_info.index in is_tools:
                            if slot_item.info.is_clean():
                                one = cursor_item.extract_item(1)
                                slot_item.add_item(one)
                        else:
                            one = cursor_item.extract_item(1)
                            slot_item.add_item(one)

            self.right_click.invoke()
        else:
            super().on_mouse_stay(pos)
        if not self.item.info.is_zero() and self.description_object.show_description.run_periodic_task():
            self.description_object.location.visible = True
            self.description_object.set_item(self.item.info.index)

    def start(self):
        super().start()
        self.inventory: 'InventoryWindow' = Manger.scene.get_object("inventory")

    def on_mouse_exit(self, pos: tuple[int, int]):
        super().on_mouse_exit(pos)
        self.description_object.location.visible = False

    def slot_click(self):
        cursor_item: ItemUI = self.cursor.location.children[0].object
        cursor_info: ItemInfo = cursor_item.info
        slot_item = self.item
        slot_info: ItemInfo = slot_item.info

        if cursor_info.index == slot_info.index and not cursor_info.is_clean():
            if cursor_info.index not in is_tools:
                slot_item.add_item(cursor_info)
                cursor_item.clear()
        else:
            copy_info = cursor_info.copy()
            cursor_item.set_item(slot_info)
            slot_item.set_item(copy_info)

    def setup(self, description_object, cursor):
        self.cursor: ItemCursor = cursor
        self.description_object: 'ItemDescription' = description_object
        self.item.on_change_count()


class ResultSlot(Button):
    def __init__(self, name, position, parent_name, default, item_index, count):
        super().__init__(name, 6, "slot", True, position, 0, parent_name, default, size=(3, 3))
        
        self.is_click.add_lisner(self.slot_click)
        image = self.get_image(item_index)
        self.item = ItemUI(name+"_item", 7, [0, 0], name, image, item_index, count)
        self.childrens.append(self.item)

        self.is_click.add_lisner(self.on_change_event)

    def on_change_event(self):
        if self.item.info.is_clean():
            self.description_object.location.visible = False
        else:
            self.description_object.show_description.reset()
            if self.description_object.location.visible:
                self.description_object.set_item(self.item.info.index)

    def start(self):
        super().start()
        self.inventory: 'InventoryWindow' = Manger.scene.get_object("inventory")

    def get_image(self, item_index):
        if item_index != None:
            return Manger.tile_sheet["item"].surfaces[item_index]
        else:
            return None


    def on_mouse_enter(self, pos: tuple[int, int]):
        self.description_object.show_description.reset()

    def on_mouse_stay(self, pos: tuple[int, int]):
        super().on_mouse_stay(pos)

        if Input.get_mouse_down(2):
            slot_item = self.item

            if pygame.key.get_mods() & pygame.KMOD_SHIFT and not slot_item.info.is_clean():
                info = self.item.extract_item(self.item.info.count)
                self.inventory.add_item(info.index, info.count, info.durability)
                self.window.create_item()

        if not self.item.info.is_zero() and self.description_object.show_description.run_periodic_task():
            self.description_object.location.visible = True
            self.description_object.set_item(self.item.info.index)


    def on_mouse_exit(self, pos: tuple[int, int]):
        super().on_mouse_exit(pos)
        self.description_object.location.visible = False

    def slot_click(self):
        cursor_item: ItemUI = self.cursor.location.children[0].object
        cursor_info: ItemInfo = cursor_item.info
        slot_item = self.item
        slot_info: ItemInfo = slot_item.info

        if not slot_info.is_clean():
            if cursor_info.is_clean():
                cursor_item.set_item(slot_info)
                slot_item.clear()
                self.window.create_item()
            else:
                if cursor_info.index == slot_info.index:
                    if cursor_info.index not in is_tools:
                        cursor_item.add_item(slot_info)
                        slot_item.clear()
                        self.window.create_item()

    def setup(self, window, description_object, cursor):
        self.cursor: ItemCursor = cursor
        self.window = window
        self.description_object = description_object
        self.item.on_change_count()

class HotBarSlot(GameObject):
    def __init__(self, name, layer, position, parent_name, item_index, count):
        super().__init__(name, layer, "slot", True, position, 0, parent_name)

        self.image = ImageObject(self, path="./resource/inventoryItemIcons/itemSlot.png", follow=True, size=(3, 3))
        self.components.append(self.image)

        image = self.get_image(item_index)

        self.item = ItemUI(name+"_item", layer, [0, 0], name, image, item_index, count)
        self.childrens.append(self.item)

    def synchronization(self, info: ItemInfo):
        self.item.set_item(info)

    def get_image(self, item_index):
        if item_index != None:
            return Manger.tile_sheet["item"].surfaces[item_index]
        else:
            return None

    def setup(self):
        self.item.on_change_count()

class CursorItemUI(UI):
    def __init__(self, name, position, parent_name, item_index, count):
        super().__init__(name, 8, "item", True, position, 0, parent_name)
        self.image = ImageObject(self, value=self.get_image(item_index), follow=True)
        self.components.append(self.image)

        self.info = ItemInfo(
            item_index,
            count,
            is_tools.get(item_index, None)
        )

    def clear(self):
        self.info.clear()
        self.on_change_item()
    
    def set_item(self, info: ItemInfo):
        self.info.create_item(info)
        self.on_change_item()

    def set_item_low(self, index, count, durability=None):
        self.info.create_item_low(index, count, durability)
        self.on_change_item()

    def add_item(self, info: ItemInfo):
        if self.info.is_clean():
            self.info.create_item(info)
        else:
            self.info.add_item(info)
        self.on_change_item()

    def add_item_low(self, index, count, durability=None):
        if self.info.is_clean():
            self.info.create_item_low(index, count, durability)
        else:
            self.info.add_item_low(count)
        self.on_change_item()

    def extract_item(self, value):
        extracted = self.info.extract_item(value)
        self.on_change_item()
        return extracted

    def sub_item(self, count):
        self.info.sub_item_low(count)
        self.on_change_item()

    def on_change_item(self):
        self.image.og_image = self.get_image(self.info.index)

    def get_image(self, item_index):
        if item_index != None:
            return Manger.tile_sheet["item"].surfaces[item_index]
        else:
            return None
        
class ItemUI(UI):
    def __init__(self, name, layer, position, parent_name, item, item_index, count):
        super().__init__(name, layer, "item", True, position, 0, parent_name)
        
        self.info = ItemInfo(
            item_index,
            count,
            is_tools.get(item_index, None)
        )

        self.on_change_event = Event()

        self.image = ImageObject(self, value=item, follow=True)

        self.text = Text(name+"_text", layer,"text", True, [20, -5], 0, name, 16, (255, 255, 255), "./font/DungGeunMo.ttf", 2, render_type="topright", shadow=(0, 0, 0))
        self.childrens.append(self.text)

    def start(self):
        self.image.start()

    def update(self):
        self.image.update()

    def render(self, surface: Surface, camera):
        self.image.render(surface, camera)
        if self.info.durability != None:
            cameraed = camera.centerXY(self.render_position)
            w, h = self.image.og_image.get_size()
            color = (51, 255, 51)
            if self.info.durability < 60:
                color = (255, 250, 105)
            elif self.info.durability < 30:
                color = (255, 38, 38)
            pygame.draw.rect(surface, color, pygame.Rect(cameraed.x-w // 2 + 8, cameraed.y+h // 2 - 8, int(self.info.durability / 3 ), 3))

    def clear(self):
        self.info.clear()
        self.on_change_item()
    
    def set_item(self, info: ItemInfo):
        self.info.create_item(info)
        self.on_change_item()

    def set_item_low(self, index, count, durability=None):
        self.info.create_item_low(index, count, durability)
        self.on_change_item()

    def add_item(self, info: ItemInfo):
        if self.info.is_clean():
            self.info.create_item(info)
        else:
            self.info.add_item(info)
        self.on_change_item()

    def add_item_low(self, index, count, durability=None):
        if self.info.is_clean():
            self.info.create_item_low(index, count, durability)
        else:
            self.info.add_item_low(count)
        self.on_change_item()

    def extract_item(self, value: int):
        extracted = self.info.extract_item(value)
        self.on_change_item()
        return extracted

    def sub_item(self, count):
        self.info.sub_item_low(count)
        self.on_change_item()

    def get_image(self, item_index):
        if item_index != None:
            return Manger.tile_sheet["item"].surfaces[item_index]
        else:
            return None

    def on_change_item(self):
        self.image.set_orginal_image(self.get_image(self.info.index))
        if self.info.index in is_tools:
            self.text.location.visible = False
        else:
            self.text.location.visible = True
        self.on_change_count()
    
    def on_change_count(self):
        self.text.text = f"{self.info.count}"

        if self.info.index in is_tools:
            self.text.location.visible = False
        else:
            self.text.location.visible = True

        if self.info.is_zero():
            self.location.visible = False
        else:
            self.location.visible = True
        
        self.on_change_event.invoke(self.info.copy())