from pygameHelper import (
    GameObject, 
    ImageObject, 
    Animation, 
    AnimationManager, 
    Vector
)

from objects.particle import Particle

import random

class Wing(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self)
        self.components.append(self.image)

        self.ready_animation = Animation(30, self.image, sheet="playerWingReady", once=True)
        jump_animation =       Animation(40, self.image, sheet="playerWingJump",  once=True)

        self.animation_manager = AnimationManager(self, {
            "ready": self.ready_animation,
            "jump": jump_animation
        }, "jump")

        self.components.append(self.animation_manager)
        def jump():
            self.animation_manager.change_animation("jump")
            particle = FeatherParticle("feathers", self.location.world_position)
            particle.instantiate()

        self.ready_animation.on_end.add_lisner(jump)
        self.use = False

    def start_animation(self):
        self.animation_manager.change_animation("ready")

class FeatherParticle(Particle):
    def __init__(self, name, position):
        super().__init__(name, position)
        self.image = ImageObject(self)
        self.components.append(self.image)

        self.animation = Animation(50, self.image, sheet="wingParticle", once=True)
        self.components.append(self.animation)

        self.animation.on_end.add_lisner(self.delete)

    def update(self):
        self.location.translate(Vector(2*(0.5-random.random()), -2))