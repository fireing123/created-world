import pygame
from pygameHelper import (
    UI, 
    Text, 
    game, 
    TEXTEDITING, 
    Manger
)

class KorWarning(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.text = Text(name+"_text", layer, "text", True, [0, 0], 0, name, 25, [255, 0, 0, 0], "./font/DungGeunMo.ttf", 2, render_type="center")
        self.childrens.append(self.text)
        self.text.text = "한글로 입력중!!!\n영어키로 바꾸세요!"
        self.speed = 3
        game.event_event.add_lisner(self.event)

    def update(self):
        color = self.text.color.copy()
        color[3] = int(pygame.math.lerp(color[3], 0, min(1, Manger.delta_time * self.speed)))    
        self.text.color = color

    def event(self, event: pygame.event.Event):
        if event.type == TEXTEDITING:
            if event.text != "":
                color = self.text.color.copy()
                color[3] = 255
                self.text.color = color