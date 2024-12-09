from pygameHelper import (
    GameObject, 
    TimerTask, 
    Manger, 
    ImageObject, 
    Animation
)

from objects.cow        import Cow
from objects.chicken    import Chicken
from objects.alotabones import Bones
from objects.zombie     import Zombie
from objects.slime      import Sime

import random

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.night import Night

class Creater(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self)
        self.components.append(self.image)

        self.idle_animation = Animation(200, self.image, sheet="touch")
        self.components.append(self.idle_animation)

        self.next = TimerTask(10000)

        self.deaths = 0
        self.lives = 0

        self.index = 0

    @property
    def uuid(self):
        self.index += 1
        return self.index

    def get_attribute(self, tag):
        return self.name + f'_created_{self.uuid}', self.layer, tag, True, self.location.world_position, 0, "parent"

    def update(self):
        if self.night.get_time() == 0:
            if self.lives == 0:
                if self.next.run_periodic_task():
                    for i in range(random.choice([0, 2, 3, 1, 0])):
                        cow = Cow(*self.get_attribute('living'))
                        cow.die_event.add_lisner(self.created_death)
                        cow.instantiate()
                        self.lives += 1

                    for i in range(random.choice([0, 2, 3, 1, 0])):
                        chicken = Chicken(*self.get_attribute('living'))
                        chicken.die_event.add_lisner(self.created_death)
                        chicken.instantiate()
                        self.lives += 1
        else:
            if self.deaths == 0:
                if self.next.run_periodic_task():
                    for i in range(random.choice([0, 2, 3, 1, 0])):
                        zombie = Zombie(*self.get_attribute('notliving'))
                        zombie.die_event.add_lisner(self.created_destroy)
                        zombie.instantiate()
                        self.deaths += 1
    
                    for i in range(random.choice([0, 2, 3, 1, 0])):
                        bone = Bones(*self.get_attribute('notliving'))
                        bone.die_event.add_lisner(self.created_destroy)
                        bone.instantiate()
                        self.deaths += 1 
                    
                    for i in range(random.choice([0, 2, 3, 1, 0])):
                        slime = Sime(*self.get_attribute('notliving'))
                        slime.die_event.add_lisner(self.created_destroy)
                        slime.instantiate()
                        self.deaths += 1
    
    def created_destroy(self):
        self.next.reset()
        self.deaths -= 1

    def created_death(self):
        self.next.reset()
        self.lives -= 1

    def start(self):
        self.night: 'Night' = Manger.scene.get_object("night")