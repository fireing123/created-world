from pygameHelper import (
    UI,
    ImageObject,
    Text,
    Button,
    Game,
    Manger
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.UI.InventoryUI import InventoryWindow

class PauseUI(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, path="./resource/ui/wyname.png", size=(3, 3), follow=True, collide=True)
        self.components.append(self.image)
        
        self.info = Text(name+"_text", layer, "text", True, [0 ,100], 0, name, 30, (0, 0, 0), "./font/DungGeunMo.ttf", 5, render_type="center")
        self.childrens.append(self.info)
        self.info.text = "일시정지"

        self.button = Button(name+"_button", layer, "tag", True, [0, -10], 0, name, "./resource/inventory/signs/button.png")
        self.childrens.append(self.button)
        self.button.is_click.add_lisner(self.ress)

        self.button_text = Text(name+"_button_text", layer, "text", True, [0 ,0], 0, name+"_button", 30, (0, 0, 0), "./font/DungGeunMo.ttf", 5, render_type="center")
        self.childrens.append(self.button_text)
        self.button_text.text = "게속하기"

        self.button = Button(name+"_ebutton", layer, "tag", True, [0, -75], 0, name, "./resource/inventory/signs/button.png")
        self.childrens.append(self.button)
        self.button.is_click.add_lisner(lambda: Game.stop("exit"))

        self.button_text = Text(name+"_ebutton_text", layer, "text", True, [0 ,0], 0, name+"_ebutton", 30, (0, 0, 0), "./font/DungGeunMo.ttf", 5, render_type="center")
        self.childrens.append(self.button_text)
        self.button_text.text = "종료"

    def start(self):
        self.inventory: 'InventoryWindow' = Manger.scene.get_object("inventory")
        self.panel = Manger.scene.get_object("pause_panel")

    def ress(self):
        if self.inventory.openning_window_type == None and not self.inventory.open_this_frame:
            self.panel.location.visible = not self.panel.location.visible
            Game.is_time_running = not self.panel.location.visible