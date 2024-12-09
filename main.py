import pygame
import os
import sys

# 어떻게든 실행되게 하는
os.chdir(
    os.path.abspath(os.path.dirname(__file__)) # 상대 경로를 이 폴더 기준으로 변경한다!
)
sys.path.append("./") # pygameHelper 를 임포트 가능하게 하고

from pygameHelper import *
from objects.UI.tutorialUI import TutorialUI

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.UI.InventoryUI import InventoryWindow
    from objects.UI.panel import Panel
    from objects.UI.pauseUI import PauseUI

SCREEN_SIZE = (1200, 800)
TITLE = "창작된 세계"

Game.init(SCREEN_SIZE, TITLE)

Game.import_objects("objects/", debug=None)

@game.world("scene/start.json")
def start():
    def start():
        camera: 'CameraObject' = Manger.scene.get_object("main_cam")
        camera.cam_color = (0, 108, 240)

        title: 'Text' = Manger.scene.get_object("title")
        title.render_type = "center"
        title.shadow = (0, 0, 0)
        title.shadow_pos = [4, 4]
        title.text = TITLE

        panel = Manger.scene.get_object("panel")

        def openor():
            panel.location.visible = True
            
        button = Button("start_button", 4, "button", True, [0, 0], 0, "parent", None, surface=(200, 60))
        button.is_click.add_lisner(openor)
        button.instantiate()

        button_text = Text("button_text", 5, "text", True, [0, 0], 0, "start_button", 45, (255, 255, 255), "./font/DungGeunMo.ttf", 0, render_type="center")
        button_text.shadow = (0, 0, 0)
        button_text.shadow_pos = [2, 2]
        button_text.text = "시작하기"
        button_text.instantiate()

        button = Button("end_button", 4, "button", True, [0, -100], 0, "parent", None, surface=(200, 60))
        button.is_click.add_lisner(lambda: Game.stop("exit"))
        button.instantiate()

        button_text = Text("end_button_text", 5, "text", True, [0, 0], 0, "end_button", 45, (255, 255, 255), "./font/DungGeunMo.ttf", 0, render_type="center")
        button_text.shadow = (0, 0, 0)
        button_text.shadow_pos = [2, 2]
        button_text.text = "종료"
        button_text.instantiate()

    def event(event):
        ...
    def update():
        ...
    return start, event, update

inventory: 'InventoryWindow'
panel: 'Panel'
pause_ui: 'PauseUI'

@game.world("scene/main.json")
def main(reson):
    def start():
        global inventory
        global panel
        global pause_ui
        pause_ui = Manger.scene.get_object("paus")
        panel = pause_ui.location.parent.object
        inventory = Manger.scene.get_object("inventory")
        signs = Manger.scene.get_object("sig")
        if reson == "tutorial":
            tutorial = TutorialUI("tutorial", 4, "ui", True, [-1200, 380], 0, "parent")
            tutorial.instantiate()
        
        inventory.open_with('signs')

        signs.talk_start("real_first_message")
    def event(event: pygame.event.Event):
        ...

    def update():
        if Input.get_key_down(K_ESCAPE):
            if inventory.openning_window_type == None:
                panel.location.visible = not panel.location.visible
                Game.is_time_running = not panel.location.visible
                if Game.is_time_running:
                    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() * 3)
                    pygame.mixer.unpause()
                else:
                    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() * 0.33333)
                    pygame.mixer.pause()

    return start, event, update

reson = None

while reson not in ["exit", "quit"]:
    reson = start()

    if reson in ["next", "tutorial"]:
        reson = main(reson)

pygame.quit() # idle 로 실행시 종료가 정상적으로 안됨 (idle 특성상) 창이라도 닫아서 종료 했다는걸 나타냄