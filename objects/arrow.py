from pygameHelper import (
    GameObject, 
    ImageObject, 
    Physics, 
    Rect,
    Vector, 
    TimerTask,
    Manger
)

from components.hitObject import Attacker
from components.inventory import ItemIndex

class NomalArrow(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, **kwargs):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, value=Manger.surface_sheet["arrrow"].images[0])
        self.image.set_flip(True)
        self.components.append(self.image)

        self.physics = Physics(self, Rect(0, 0, 15, 15))
        self.physics.collision_enter_event.add_lisner(self.collision_enter)
        self.physics.air_friction = 0.001
        self.components.append(self.physics)

        self.rect = Rect(0, 0, 15, 15)

        self.death_time = TimerTask(10000)
        self.now_his_died = False

        self.ignore_tag = kwargs.get("ignore_tag", None)

    def collision_enter(self, collision, collision_type):
        if not self.now_his_died:
            self.physics.delete()
            self.now_his_died = True
            self.death_time.reset()

    def setup(self, host):
        self.attacker = Attacker(self, self.rect, except_object=host)
        self.components.append(self.attacker)

    def update(self):
        self.rect.center = self.location.world_position
        if self.now_his_died:
            if self.death_time.run_periodic_task():
                self.delete()
        elif not (self.physics.velocity.x == 0 == self.physics.velocity.y):
            angle = Vector(0, 0).angle_to(self.physics.velocity) + 180
            self.location.rotation = angle
            hits = self.attacker.hit_check(ItemIndex.ARROW, 20, self.ignore_tag)

            for hit_object in hits:
                if hit_object.object.tag in ["living", "notliving"]:
                    try:
                        self.not_ground_delete()
                    except: pass
                    break

    def delete(self):
        if self.physics.on_ground:
            super().delete()

    def not_ground_delete(self):
        super().delete()