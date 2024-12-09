from pygameHelper import *

from components.signs import world_list, create_beep
from components.windowManager import WindowManager

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.player         import Player
    from objects.followCamera   import FollowCamera
    from objects.UI.InventoryUI import InventoryWindow

class WorldVoice(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)

        self.image = ImageObject(self, surface=[Manger.WIDTH, Manger.HEIGHT], follow=True, type='center', collide=True)
        self.image.og_image.fill((0, 0, 0))
        self.components.append(self.image)

        self.window_manager = WindowManager(self, "world")
        
        self.window_manager.on_open.add_lisner(self.on_open)
        self.window_manager.on_close.add_lisner(self.on_close)

        self.text = Text(name+"_text", layer, "text", True, [0, 0], 0, name, 45, (255, 255, 255), "./font/DungGeunMo.ttf", 5, render_type="center")
        self.childrens.append(self.text)

        self.index = 0
        self.script = None
        self.script_name = ""
        self.is_running = False

        self.wait_task = TimerTask(100)
        self.value_index = 0
        self.value = None

        self.is_next = False
        self.on_end = Event()
        self.next_moment = TimerTask(0)

        self.sound_manager = SoundManager({
            "world": SoundSource(self, create_beep(100, 0.15), 0, lambda dist: 0.1)
        })

        self.end_event = None

    def update(self):
        if self.is_running:
            if self.wait_task.run_periodic_task():
                
                if self.value_index != len(self.value):
                    char = self.value[self.value_index]
                    self.value_index += 1

                    if char == "@": # fast
                        self.wait_task.tick -= 25
                    elif char == "*":# low fast
                        self.wait_task.tick -= 5
                    elif char == "$": #lower
                        self.wait_task.tick += 25
                    elif char == "%": # close
                        self.wait_task.tick = 100
                    else:
                        if char != " ":
                            self.sound_manager.play("world")
                        self.text.text += char
                else:
                    if not self.is_next:
                        self.is_next = True
                        self.on_end.invoke(self.script_name, self.index)
                        self.next_moment.reset()
            if self.is_next:
                if self.next_moment.run_periodic_task():
                    self.next_script()

    def start(self):
        try:
            self.inventory = Manger.scene.get_object("inventory")
            self.player: 'Player' = Manger.scene.get_object("player")
        except:
            pass

    def on_open(self, inventory_ui: 'InventoryWindow'):
        self.location.visible = True
        inventory_ui.location.visible = False
        self.player.change_animation("auto", key=self.player.animation_manager.state)

    def on_close(self, inventory_ui: 'InventoryWindow'):
        self.location.visible = False
        inventory_ui.location.visible = True

    def talk_start(self, name, end_event=None): # 여기서 end_event 란 함수고 대화가 끝나고 실행됨을 의미한다
        c: 'FollowCamera' = Manger.scene.camera
        c.map_stop = True
        self.end_event = end_event
        self.location.visible = True
        self.script_name = name
        self.script = world_list[name]
        try:
            self.inventory.open_with("world")
        except: pass
        self.index = 0
        self.next_script()

    def animation_text_start(self, value):
        self.is_running = True
        self.value = value
        self.text.text = ""
        self.value_index = 0

    def next_script(self):
        self.is_next = False
        if self.index != len(self.script):
            tick, value = self.script[self.index]
            self.next_moment.tick = tick
            self.animation_text_start(value)
            self.index+=1
        else:
            self.is_running = False
            self.location.visible = False
            c: 'FollowCamera' = Manger.scene.camera
            c.map_stop = False
            if self.end_event != None:
                self.end_event()
            try:
                self.inventory.close()
            except: pass