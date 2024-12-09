from pygameHelper import (
    ImageObject, 
    Physics, 
    Manger, 
    OnceTimerTask,
    Rect
)

from objects.particle import Particle

import random

class PixelParticle(Particle):
    def __init__(self, name, position, velcoity, sheet, index):
        super().__init__(name, position)
        self.image = ImageObject(self, value=Manger.tile_sheet[sheet].surfaces[index])
        self.components.append(self.image)

        self.physics = Physics(self, Rect(0, 0, 4, 4))
        self.components.append(self.physics)
        self.physics.velocity = velcoity
        self.physics.collision_enter_event.add_lisner(self.on_collison_stay)

        self.wait = OnceTimerTask(300+random.random()*100)
        self.wait.once = True

    def update(self):
        if self.wait.run_periodic_task():
            self.delete()
    
    def on_collison_stay(self, rect, col_type):
        if self.wait.once:
            self.wait.reset()
