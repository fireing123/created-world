from pygameHelper import (
    UI, 
    ImageObject, 
    Manger
)

class PanelC(UI):
    def __init__(self, name, tag, visible, parent_name):
        super().__init__(name, 5, tag, visible, [0, 0], 0, parent_name)
        self.image = ImageObject(self, surface=[Manger.WIDTH, Manger.HEIGHT], follow=True, type='center')
        self.image.og_image.fill((0, 0, 0))
        self.components.append(self.image)
