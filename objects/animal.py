from pygameHelper import (
    GameObject,
    TimerTask
)

from objects.livingObject import LivingObject

class Aniaml(LivingObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, heath, rect):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name, heath, rect)
        self.is_walk = False
        self.is_left = False

        self.next_moment = TimerTask(1000)
        self.cry_moment = TimerTask(3000)

    def runaway(self, object: GameObject):
        if object.location.world_position.x >= self.location.world_position.x:
            self.is_left = True
            self.is_walk = True
        else:
            self.is_left = False
            self.is_walk = True