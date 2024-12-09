from pygameHelper import (
    GameObject,
    Physics, 
    Rect,
    Event,
    Vector,
    TimerTask
)

from components.hitObject import HitComponent

class LivingObject(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, heath, rect: Rect):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.max_heath = heath
        self.heath= heath

        self.rect : Rect = rect

        self.invincibility = TimerTask(100)

        self.hit_checker = HitComponent(self, rect)
        self.components.append(self.hit_checker)

        self.physics = Physics(self, self.rect)
        self.components.append(self.physics)

        self.die_event = Event()

    def walk(self, direction: bool, power: float, limit: float):
        """direction true 가 왼쪽 
        false가 오른쪽"""
        if direction:
            if self.physics.velocity.x > -limit:
                self.physics.add_force(Vector(-power, 0))
        else:
            if self.physics.velocity.x < limit:
                    self.physics.add_force(Vector(power, 0))

    def knockback(self, other: GameObject, vector: Vector):
        if other.location.world_position.x >= self.location.world_position.x:
                vector = vector.copy()
                vector.x *= -1
        self.physics.velocity = vector