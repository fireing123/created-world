from pygameHelper import (
    UI, 
    mouse, 
    Vector,
    Manger
)

class ItemCursor(UI):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)

    def update(self):
        render_pos = Vector(mouse.inget_pos())
        render_pos.y *= -1
        render_pos.y += Manger.HEIGHT
        self.location.position = render_pos