from pygameHelper import (
    GameObject, 
    ImageObject, 
    Manger, 
    Vector
)

class Cloud(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, index, speed):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, value=Manger.surface_sheet["cloud"].images[index])
        self.components.append(self.image)
        self.speed = speed

    def update(self):
        if self.location.position.x > 2000:
            self.delete()
        self.location.translate(Vector(self.speed, 0))