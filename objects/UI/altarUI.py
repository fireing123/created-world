from pygameHelper import (
    UI, 
    ImageObject, 
    Manger, 
    Vector
)

from objects.UI.itemUI import InventorySlot

from components.itemInfo import ItemInfo
from components.inventory import ItemIndex
from components.windowManager import WindowManager

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.player         import Player
    from objects.followCamera   import FollowCamera
    from objects.UI.InventoryUI import InventoryWindow

class AltarUI(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, path="./resource/boss/bosscallor.png", size=(5, 5), follow=True)
        self.components.append(self.image)

        self.window_manager = WindowManager(self, "altar")
        
        self.window_manager.on_open.add_lisner(self.on_open)
        self.window_manager.on_close.add_lisner(self.on_close)

        self.material_slot = InventorySlot(name+"_slot", [0, 70], name, "./resource/inventoryItemIcons/itemSlot.png", None, 0)
        self.childrens.append(self.material_slot)

        self.material_slot.item.on_change_event.add_lisner(self.call)

        self.real_once = True
        self.fake_once = True

    def start(self):

        self.player: 'Player' = Manger.scene.get_object("player")
        self.description_object=Manger.scene.get_object("description")
        self.cursor =           Manger.scene.get_object("ItemCursor")

        self.material_slot.setup(self.description_object, self.cursor)

        self.real_boss =        Manger.scene.get_object("realboss")
        self.fake_boss =        Manger.scene.get_object("fakeboss")


    def on_open(self, inventory_ui: 'InventoryWindow'):
        self.location.visible = True

    def on_close(self, inventory_ui: 'InventoryWindow'):
        self.location.visible = False

    def call(self, info: ItemInfo):
        match info.index:
            case ItemIndex.GOD_CALLOR:
                if not self.real_once:
                    self.player.world_1.talk_start("not_boss_world")                    
                    return

                if self.fake_once:
                    self.fake_once = False
                    self.player.world_1.talk_start("boss_world", lambda:self.fake_boss.start_boss())
                else:
                    self.player.world_1.talk_start("re_boss_world", lambda:self.fake_boss.start_boss())
            case ItemIndex.WORLD_GETTER:
                if self.real_once:
                    self.real_once = False
                    self.player.world_1.talk_start("real_boss_world", lambda:self.real_boss.start_boss())
                else:
                    self.player.world_1.talk_start("re_real_boss_world", lambda:self.real_boss.start_boss())
            case _:
                return
        c: 'FollowCamera' = Manger.scene.camera
        c.change_sound("clear_boss")
        self.location.visible = False
        self.material_slot.item.clear()
        self.player.save_point = Vector(1700, 1200)