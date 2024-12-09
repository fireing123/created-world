import pygame
from pygameHelper import (
    Text, 
    UI, 
    Surface,
    Rect,
    OnceTimerTask
)

from components.inventory import itemDescriptions

class ItemDescription(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)

        self.title = Text(name+"_title", 9, "text", True, [15, -5], 0, name, 15, (255, 255, 255), "./font/DungGeunMo.ttf", 2)
        self.childrens.append(self.title)

        self.text = Text(name+"_text", 9, "text", True, [5, -30], 0, name, 15, (255, 255, 255), "./font/DungGeunMo.ttf", 2)
        self.childrens.append(self.text)

        self.show_description = OnceTimerTask(500)
        self.text_len = 0
    
    def set_item(self, item_index):
        title, description = itemDescriptions[item_index]
        self.title.text = title
        self.text.text = description
        
        self.text_len = self.text.get_line(-1)
    
    def render(self, surface: Surface, camera):
        pos = camera.centerXY(self.render_position)
        pygame.draw.rect(surface, (0, 0, 128), Rect(pos.x-3, pos.y-3, 346, 17*self.text_len+46), 0, 10)
        pygame.draw.rect(surface, (0, 0, 0), Rect(pos.x, pos.y, 340, 17*self.text_len+40), 0, 10)