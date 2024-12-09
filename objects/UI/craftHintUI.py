from pygameHelper import (
    UI, 
    ImageObject, 
    Manger, 
    Vector, 
    Button, 
    Text
)

from components.inventory import (
    ItemIndex, 
    craft_recipe, 
    is_tools, 
    itemDescriptions
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.UI.racipeUI import RacipeUI

class CraftHint(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        
        self.data: list[list[HintSlot]] = []

        pospos = Vector(0, -200)

        interval = 48
        for i in range(3):
            cache = []
            for j in range(3):

                pos = Vector(j, i) - Vector(1, -1.5)

                pos *= interval

                pos += pospos

                slot = HintSlot(name+f"_slot_{j}-{i}", layer, "slot", True, pos, 0, name)
                self.childrens.append(slot)

                cache.append(slot)
            self.data.append(cache)

        self.result_slot = HintSlot(name+"_result", layer, "slot", True, [0, 60], 0, name)
        self.childrens.append(self.result_slot)

        self.next_button = Button(name+"_next", layer, "button", True, [80, 20], 0, name, "./resource/ui/arrow.png", size=(3, 3))
        self.next_button.image.flip[0] = True
        self.childrens.append(self.next_button)
        self.next_button.is_click.add_lisner(self.next_arrow)
        
        self.before_button = Button(name+"_before", layer, "button", True, [-80, 20], 0, name, "./resource/ui/arrow.png", size=(3, 3))
        self.childrens.append(self.before_button)
        self.before_button.is_click.add_lisner(self.before_arrow)
        
        self.text = Text(name+"_text", layer, "text", True, [0, 20], 0, name, 20, (255, 255, 255), "./font/DungGeunMo.ttf", 0, render_type="center")
        self.childrens.append(self.text)
        self.text.text = ""

        self.get_racipe = [(ItemIndex.PICKAXE, 1), (ItemIndex.AXE, 1)]
        self.racipe_index = 0

    def start(self):
        self.alarm: 'RacipeUI' = Manger.scene.get_object("alram")
        self.change_hint(0)

    def extend_racipe(self, list):
        self.get_racipe.extend(list)
        for index, count in list:
            self.alarm.on_get_racipe(index)

    def change_hint(self, index):
        dict_key = self.get_racipe[index]
        result_index, count = dict_key
        self.result_slot.set_item(result_index, count)
        self.text.text = itemDescriptions[result_index][0]
        racipe = craft_recipe[dict_key]
        for i in range(3):
            for j in range(3):
                self.data[i][j].set_item(*racipe[i][j])

    def next_arrow(self):
        self.racipe_index += 1

        if self.racipe_index == len(self.get_racipe):
            self.racipe_index = 0
        self.change_hint(self.racipe_index)
    
    def before_arrow(self):
        self.racipe_index -= 1

        if self.racipe_index == -1:
            self.racipe_index = len(self.get_racipe) - 1
        self.change_hint(self.racipe_index)
        
class HintSlot(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)

        self.image = ImageObject(self, follow=True)
        self.components.append(self.image)

        self.text = Text(name+"_text", layer,"text", True, [15, -5], 0, name, 15, (255, 255, 255), "./font/DungGeunMo.ttf", 2, render_type="topright")
        self.childrens.append(self.text)

    def set_item(self, item_index, count):
        if item_index != None:
            self.image.og_image = Manger.tile_sheet["item"].surfaces[item_index]
        else:
            self.image.og_image = None

        self.text.text = f"{count}"

        if item_index in is_tools:
            self.text.location.visible = False
        else:
            self.text.location.visible = True

        if count == 0:
            self.location.visible = False
        else:
            self.location.visible = True