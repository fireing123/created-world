from pygameHelper import *

from components.inventory import itemDescriptions
from objects.UI.itemUI import HotBarSlot
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from objects.UI.InventoryUI import InventoryWindow
    from objects.UI.itemUI import InventorySlot
    
class HotBar(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)

        self.slots = []

        for i in range(-3, 3):
            hotbar_slot = HotBarSlot(name+f"_slot_{i}", layer, [48*i, 0], name, None, 0)
            self.childrens.append(hotbar_slot)
            self.slots.append(hotbar_slot)

        self.focus_slot = FocusHotBar(name+"_focus", layer, "focus", True, [0, 0], 0, name)
        self.childrens.append(self.focus_slot)

        self.item_text = Text("qhotbar", layer, "text", True, [-24, 85], 0, name, 20, [255, 255, 255, 0], "./font/DungGeunMo.ttf", 5, render_type="center", shadow=(0, 0, 0, 0))
        self.childrens.append(self.item_text)

        self.focus_slot.on_changed_focus.add_lisner(self.on_changed_focus)

        self.wait = OnceTimerTask(2000)
        self.speed = 6

        self.visible = False

    def on_changed_focus(self, focus_index):
        item_index = self.get_focuse_slot().item.info.index
        self.visible = True
        if item_index in itemDescriptions:
            self.item_text.text = itemDescriptions[item_index][0]
        else:
            self.item_text.text = ""
            self.visible = False
        self.wait.reset()

    def get_focuse_slot(self) -> 'InventorySlot':
        return self.inventory.data[0][self.focus_slot.focus_index]

    def start(self):
        self.inventory: 'InventoryWindow' = Manger.scene.get_object("inventory")

        for i in range(6):
            self.slots[i].setup()
            self.inventory.data[0][i].item.on_change_event.add_lisner(self.slots[i].synchronization)

    def update(self):
        if self.wait.run_periodic_task():
            self.visible = False

        color = self.item_text.color.copy()
        if self.visible:
            color[3] = int(pygame.math.lerp(color[3], 255, min(1, Manger.delta_time * self.speed)))
        else:
            color[3] = int(pygame.math.lerp(color[3], 0, min(1, Manger.delta_time * self.speed)))    
        self.item_text.color = color


class FocusHotBar(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, path="./resource/inventoryItemIcons/focusHotbar.png", follow=True, size=(3.4, 3.4))
        self.components.append(self.image)
        self.focus_index = 0
        self.on_changed_focus = Event()
        game.event_event.add_lisner(self.event)

    def start(self):
        self.focus(4)

    def focus(self, index):
        if index != self.focus_index:
            vec = Vector(48, 0)
            self.location.position = vec * (index - 3)
            self.focus_index = index
            self.on_changed_focus.invoke(index)

    def event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                if self.focus_index == 0:
                    self.focus(5)
                else:
                    self.focus(self.focus_index-1)

            elif event.y == -1:
                if self.focus_index == 5:
                    self.focus(0)
                else:
                    self.focus(self.focus_index+1)

    def update(self):
        if Input.get_key_down(pygame.K_1):
            self.focus(0)
        elif Input.get_key_down(pygame.K_2):
            self.focus(1)
        elif Input.get_key_down(pygame.K_3):
            self.focus(2)
        elif Input.get_key_down(pygame.K_4):
            self.focus(3)
        elif Input.get_key_down(pygame.K_5):
            self.focus(4)
        elif Input.get_key_down(pygame.K_6):
            self.focus(5)