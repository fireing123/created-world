from pygameHelper import GameObject, ImageObject

class DecImage(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, path, size):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, path=path, size=size)
        self.components.append(self.image)