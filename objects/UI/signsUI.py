from pygameHelper import *

from components.signs           import talk_list, create_beep
from components.inventory       import ItemIndex
from components.windowManager   import WindowManager

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.player         import Player
    from objects.UI.InventoryUI import InventoryWindow
    from objects.UI.craftHintUI import CraftHint

class SignsUI(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, path="./resource/inventory/signs/Signs.png", follow=True, size=(6.6, 6.6), collide=True)
        self.components.append(self.image)

        self.window_manager = WindowManager(self, "signs")
        
        self.window_manager.on_open.add_lisner(self.on_open)
        self.window_manager.on_close.add_lisner(self.on_close)

        self.player_side = SignsName(name+"_ps", layer, "signs", True, [-412, 145], 0, name, "./resource/inventory/signs/leftSigns.png")
        self.childrens.append(self.player_side)

        self.other_side = SignsName(name+"_os", layer, "signs", True, [412, 145], 0, name, "./resource/inventory/signs/rightSigns.png")
        self.childrens.append(self.other_side)

        self.text = Text(name+"_value", layer, "text", True, [-490, 90], 0, name, 20, [0, 0, 0], "./font/DungGeunMo.ttf", 5)
        self.childrens.append(self.text)
        
        self.next_button = Button(name+"_next", layer, "button", True, [440, -80], 0, name, "./resource/inventory/signs/button.png")
        self.childrens.append(self.next_button)
        self.next_button.is_click.add_lisner(self.next_script)

        self.next_text = Text(name+"_next_text", layer, "text", True, [-20, 8], 0, name+"_next", 20, [0, 0, 0], "./font/DungGeunMo.ttf", 5)
        self.childrens.append(self.next_text)
        self.next_text.text = "다음"

        self.index = 0
        self.script = None
        self.script_name = ""
        self.is_running = False

        self.wait_task = TimerTask(50)
        self.value_index = 0
        self.value = None
        self.voice = None

        self.on_end = Event()

        self.sound_manager = SoundManager({
            "player": SoundSource(self, create_beep(350, 0.05), 0, lambda dist: 0.1),
            "player_think": SoundSource(self, create_beep(200, 0.05), 0, lambda dist: 0.1),
            "signs": SoundSource(self, create_beep(500, 0.05), 0, lambda dist: 0.03),
            "world": SoundSource(self, create_beep(100, 0.15), 0, lambda dist: 0.03)
        })

    def on_open(self, inventory_ui: 'InventoryWindow'):
        self.location.visible = True
        inventory_ui.location.visible = False
        self.player.change_animation("auto", key=self.player.animation_manager.state)

    def on_close(self, inventory_ui: 'InventoryWindow'):
        self.location.visible = False
        inventory_ui.location.visible = True

    def on_mouse_stay(self, pos: tuple[int, int]):
        if Input.get_mouse_down(0):
            self.text.text = self.value.translate({ord(letter): None for letter in '@$%'})
            self.value_index = len(self.text.text)
    
    def update(self):
        if self.is_running:
            if self.wait_task.run_periodic_task():
                
                if self.value_index != len(self.value):
                    char = self.value[self.value_index]
                    self.value_index += 1

                    if char == "@": # fast
                        self.wait_task.tick = 30
                    elif char == "$": #lower
                        self.wait_task.tick = 150
                    elif char == "%": # close
                        self.wait_task.tick = 50
                    else:
                        if char != " ":
                            self.sound_manager.play(self.voice)
                        self.text.text += char
                else:
                    self.next_button.location.visible = True

    def start(self):
        self.player: 'Player' = Manger.scene.get_object("player")
        inventory = Manger.scene.get_object("inventory")
        self.hintor : 'CraftHint' = Manger.scene.get_object("hintor")
        self.window = inventory

    def talk_start(self, name):
        self.location.visible = True
        self.script_name = name
        self.script = talk_list[name]

        self.index = 0
        self.next_script()

    def next_script(self):
        self.next_button.location.visible = False
        if self.index != len(self.script):
            is_left_side, name, voice, value = self.script[self.index]
            self.animation_text_start(value)
            self.player_side.location.visible = is_left_side
            self.other_side.location.visible = not is_left_side
            self.voice = voice
            if is_left_side:
                self.player_side.text.text = name
            else:
                self.other_side.text.text = name
            self.index+=1
        else:
            self.is_running = False
            self.on_end.invoke(self.script_name)
            self.window.close()
            racipe = None
            match self.script_name:
                case "racipe_cave_signs":
                    racipe = [(ItemIndex.BREASTPLATE, 1), (ItemIndex.BOOTS, 1), (ItemIndex.SWORD, 1)]
                case "racipe_fly_signs":
                    racipe = [(ItemIndex.FEATHER_BUNDLE, 1), (ItemIndex.WING, 1)]
                case "racipe_bow_signs":
                    racipe = [(ItemIndex.BOW, 1), (ItemIndex.ARROW, 16)]
                case "racipe_pickaxe_signs":
                    racipe = [(ItemIndex.IRON_PICKAXE, 1)]
                case "jump_map_signs" | "god_signs":
                    racipe = [(ItemIndex.GOD_CALLOR, 1)]
                case "world_is_boss_signs":
                    racipe = [(ItemIndex.WORLD_GETTER, 1)]
                case _:
                    racipe = []
            index = 0
            length = len(racipe)
            for rac in self.hintor.get_racipe:
                for r in racipe:
                    if rac == r:
                        index += 1
                        break
                if index == length:
                    break
            else:
                self.hintor.extend_racipe(racipe)

    def animation_text_start(self, value):
        self.is_running = True
        self.value = value
        self.text.text = ""
        self.value_index = 0

class SignsName(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, image_path):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)

        self.image = ImageObject(self, path=image_path, follow=True, size=(6.6, 6.6))
        self.components.append(self.image)

        self.text = Text(name+"_text", layer, "text", True, [0, -10], 0, name, 35, (0, 0, 0), "./font/DungGeunMo.ttf", 0, render_type="center")
        self.childrens.append(self.text)