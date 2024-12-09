from pygameHelper import (
    GameObject, 
    ImageObject, 
    Manger, 
    K_e
)

from components.trigger import Trigger

class Signs(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, path="./resource/objects/signsobj.png", size=(3, 3))
        self.components.append(self.image)

        self.trigger = Trigger(self, 100, 50, K_e)
        self.trigger.on_interaction.add_lisner(self.open)
        self.components.append(self.trigger)

    def start(self):
        inventory = Manger.scene.get_object("inventory")
        self.signs = Manger.scene.get_object("sig")
        self.window = inventory

    def open(self):
        self.window.open_with('signs')
        self.signs.talk_start(self.name)