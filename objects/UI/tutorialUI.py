from pygameHelper import *

from components.inventory   import ItemIndex
from components.itemInfo    import ItemInfo
from components.door        import on_broken

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.UI.InventoryUI     import InventoryWindow
    from objects.UI.craftTableUI    import CraftTable
    from objects.UI.furnaceUI       import Furnace
    from objects.UI.signsUI         import SignsUI
    from objects.UI.altarUI         import AltarUI

class TutorialUI(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, path="./resource/ui/racipe_alarm.png", size=(12, 12), follow=True, type="topleft")
        self.components.append(self.image)

        self.text = Text(name+"_text", layer, "text", True, [30, -30], 0, name, 25, [0, 0, 0], "./font/DungGeunMo.ttf", 5, shadow=(255, 255, 255))
        self.childrens.append(self.text)

        self.index = 0
        self.visible = False
        self.wait = TimerTask(1000)
        self.hide = OnceTimerTask(2000)
        self.hide.once = True

        self.speed = 2

        self.var = ""

        self.walk_power = 0

        self.signs_count = 0

        self.signs_dict = {}

        self.get_tree = 0
        self.get_stone = 0
        self.get_ores = False

        self.create_axe = False
        self.get_ingot = False

        self.is_destory_water = False
        self.is_destory_cave = False

        self.create_wing = False
        self.create_boots = False

        self.create_wing_and_boots = 0

        self.crate_god_caller = False
        
        self.boss = False

        def on_broken_func(name):
            if name == "Wall1":
                self.is_destory_water = True
            elif name == "Wall2":
                self.is_destory_cave = True
        on_broken.add_lisner(on_broken_func)

    def set_tutorial(self, index):
        message, var, count = tutorial_list[index]
        self.message = message
        self.var = var
        self.count = count

    def start(self):
        self.window: 'InventoryWindow' = Manger.scene.get_object("inventory")
        self.craft_table: 'CraftTable' = Manger.scene.get_object("craftTable")
        self.signs: 'SignsUI' = Manger.scene.get_object("sig")
        self.furnace: 'Furnace' = Manger.scene.get_object("furnace")
        self.altar_ui: 'AltarUI' = Manger.scene.get_object("altar_ui")
        def on_add_item(index, count, dura):
            if index == ItemIndex.TREE_BRANCH:
                self.get_tree += 1
            elif index in [ItemIndex.COAL, ItemIndex. IRON_ORE]:
                self.get_ores = True
            elif index == ItemIndex.STONE:
                self.get_stone += 1
        
        self.window.on_add_item.add_lisner(on_add_item)

        def on_create_item(index, count):
            if index == ItemIndex.AXE:
                self.create_axe = True
            elif index == ItemIndex.IRON_INGOT:
                self.get_ingot = True
            elif index == ItemIndex.WING:
                if not self.create_wing:
                    self.create_wing = True
                    self.create_wing_and_boots += 1
            elif index == ItemIndex.BOOTS:
                if not self.create_boots:
                    self.create_boots = True
                    self.create_wing_and_boots += 1
            elif index == ItemIndex.GOD_CALLOR:
                self.crate_god_caller = True

        self.craft_table.on_create_item.add_lisner(on_create_item)
        self.furnace.on_create_item.add_lisner(on_create_item)

        def on_open_signs(name):
            if name not in self.signs_dict:
                self.signs_dict[name] = True
                self.signs_count += 1
        self.signs.on_end.add_lisner(on_open_signs)

        def on_altar(info: ItemInfo):
            if info.index == ItemIndex.GOD_CALLOR:
                self.boss = True
        self.altar_ui.material_slot.item.on_change_event.add_lisner(on_altar)

        self.set_tutorial(self.index)

    def update(self):
        if self.visible:
            self.location.position = self.location.position.lerp(Vector(-590, 390), min(1, Manger.delta_time * self.speed))
        else:
            self.location.position = self.location.position.lerp(Vector(-1200, 390), min(1, Manger.delta_time * self.speed))

        if self.index != len(tutorial_list):
            if self.visible:
                self.wait.reset()

            if self.wait.run_periodic_task():
                self.set_tutorial(self.index)
                self.text.color = (0, 0, 0)
                self.visible = True

        hid = False

        if self.count == None:
            hid = getattr(self, self.var, False)
            self.text.text = f"{self.message}"
        else:
            hid = getattr(self, self.var, 0) >= self.count
            self.text.text = f"{self.message}({getattr(self, self.var, 0)}/{self.count})"

        if hid and self.hide.once and self.visible:
            self.text.color = (95, 196, 47)
            self.hide.reset()

        if self.hide.run_periodic_task():
            self.wait.reset()
            self.index += 1
            self.visible = False

        if self.walk_power < 150 and (Input.get_key(K_a) or Input.get_key(K_d) or Input.get_key(K_SPACE)):
            self.walk_power += 1
        
tutorial_list = [
    ["A, D, Space로\n조작하기!", "walk_power", 150],
    ["나무 좌클릭으로 얻기!\n(우클릭으로 줍기)", "get_tree", 3],
    ["돌 뭉텅이 캐기!\n(우클릭으로 줍기)", "get_stone", 3],
    ["왼쪽 동굴에있는\n제작대를 E키로 열어\n도끼를 제작해보자!", "create_axe", None],
    ["돌곡괭이를 제작해\n오른쪽 폭포벽을 부수자!", "is_destory_water", None],
    ["폭포에서 광물을\n채굴하자!", "get_ores", None],
    ["철 원석을 화로로 제련하자!", "get_ingot", None],
    ["표지판을 전부 읽고\n다양한 레시피들을\n얻어보자!", "signs_count", 7],
    ["철곡괭이를 제작해\n동굴벽을 부수자!", "is_destory_cave", None],
    ["날개와 부츠을 제작하자!\n(동굴 표지판)", "create_wing_and_boots", 2],
    ["동굴과 산으로 올라가\n표지판을 읽어보자!", "signs_count", 11],
    ["시련 생성기를 제작하라.", "crate_god_caller", None],
    ["보스에 맞서라.", "boss", None]
]