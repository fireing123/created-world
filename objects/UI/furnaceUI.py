import pygame
from pygameHelper import UI, ImageObject, TimerTask, Manger, Event, Surface, Rect

from objects.UI.itemUI import InventorySlot, ResultSlot

from components.inventory import ItemIndex, furnace_recipe, is_fuel
from components.windowManager import WindowManager
from components.itemInfo import ItemInfo

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.UI.InventoryUI import InventoryWindow

class Furnace(UI):
    def __init__(self, name, tag, visible, position, rotation, parent_name):
        super().__init__(name, 5, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, path="./resource/inventory/furnaceUI.png", size=(3, 3), follow=True)
        self.components.append(self.image)

        self.window_manager = WindowManager(self, "furnace")
        
        self.window_manager.on_open.add_lisner(self.on_open)
        self.window_manager.on_close.add_lisner(self.on_close)

        self.data: list[InventorySlot] = []

        self.fire_power = 0
        self.need_power = 0

        self.need_visible = 0

        self.fire_time = TimerTask(100)

        self.on_create_item = Event()

        self.material_slot = InventorySlot(name+"_matreial_slot", [0, 50], name, "./resource/inventoryItemIcons/itemSlot.png", None, 0)
        self.childrens.append(self.material_slot)
        self.material_slot.item.on_change_event.add_lisner(self.on_met_change)
        self.data.append(self.material_slot)

        self.met_bar = Bar(name+"_met_bar", 5, tag, True, [-28, 0], 0, name)
        self.childrens.append(self.met_bar)

        self.fuel_slot = InventorySlot(name+"_fuel_slot", [0, -100], name, "./resource/inventoryItemIcons/itemSlot.png", None, 0)
        self.childrens.append(self.fuel_slot)
        self.fuel_slot.item.on_change_event.add_lisner(self.on_fuel_change)
        self.data.append(self.fuel_slot)

        self.bar = Bar(name+"_bar", 6, tag, True, [-28, -130], 0, name)
        self.childrens.append(self.bar)

        self.result = ResultSlot(name+"_result", [0, 200], name, "./resource/inventoryItemIcons/itemSlot.png", None, 0)
        self.childrens.append(self.result)

    def update(self):
        if self.material_slot.item.info.index in furnace_recipe:
            ind, need = furnace_recipe[self.material_slot.item.info.index]

            if self.need_power > need:
                self.need_power = 0
                self.result.item.add_item(ItemInfo(
                    ind,
                    1,
                    None
                ))

                self.material_slot.item.sub_item(1)
                self.on_create_item.invoke(ind, 1)

            self.need_visible = (100 / need) * self.need_power
        
        if self.fire_power == 0:
            if self.fuel_slot.item.info.count != 0:
                self.on_fuel_change(self.fuel_slot.item.info)
        elif self.fire_time.run_periodic_task():
            self.fire_power -= 1
            if self.material_slot.item.info.count != 0:
                if self.result.item.info.is_zero() or self.result.item.info.index == furnace_recipe.get(self.material_slot.item.info.index, [""])[0]:
                    self.need_power += 1

    def on_open(self, inventory_ui: 'InventoryWindow'):
        self.location.visible = True

    def on_close(self, inventory_ui: 'InventoryWindow'):
        self.location.visible = False

    def create_item(self):
        pass

    def on_met_change(self, info):
        self.need_power = 0

    def is_can_fire(self):
        return self.fire_power == 0 and (self.material_slot.item.info.index in furnace_recipe and (self.result.item.info.index == furnace_recipe.get(self.material_slot.item.info.index, [""])[0] or self.result.item.info.is_zero()))
    
    def on_fuel_change(self, info: ItemInfo):
        if self.is_can_fire():
            if info.index in is_fuel:
                self.fire_power = is_fuel[info.index]
                self.fuel_slot.item.sub_item(1)

    def start(self):
        self.description_object=Manger.scene.get_object("description")
        self.cursor =           Manger.scene.get_object("ItemCursor")

        self.result.setup(self, self.description_object, self.cursor)
        self.bar.setup(self, 'fire_power')
        self.met_bar.setup(self, 'need_visible')
        for slot in self.data:
            slot.setup(self.description_object, self.cursor)


class Bar(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.bar = ImageObject(self, surface=(55, 14), follow=True, type='topleft')
        self.bar.og_image.fill((127, 127, 127))

    def setup(self, furnace, name):
        self.furnace = furnace
        self.func_name = name

    def render(self, surface: Surface, camera):
        self.bar.render(surface, camera)
        x, y = camera.centerXY(self.render_position)
        pygame.draw.rect(surface, (255, 0, 0), Rect(x+2, y+2, getattr(self.furnace, self.func_name) / 2, 8))