from pygameHelper import *

from objects.livingObject import LivingObject

from components.inventory import ItemIndex
from components.itemDroper import ItemDroper
from components.hitObject import Attacker, DamageEffect
from components.itemInfo import ItemInfo
from components.livingAI import LivingMovements

import random

move = [
    LivingMovements.STOP,
    LivingMovements.STOP,
    LivingMovements.STOP,
    LivingMovements.TOGGLE,
    LivingMovements.WALK,
    LivingMovements.JUMP,
    None
]

class Sime(LivingObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name, 80, Rect(0, 0, 32, 64))
        self.image = ImageObject(self, surface=(32, 32))
        self.components.append(self.image)

        idle_animation = Animation(float('inf'), self.image, sheet="slimeIdle")
        walk_animation = Animation(200, self.image, sheet="slimeWalk")

        self.animation_manager = AnimationManager(self, {
            "idle": idle_animation,
            "walk": walk_animation
        }, 'idle')

        idle_animation.change_image()

        self.components.append(self.animation_manager)

        self.item_droper = ItemDroper(self)
        self.components.append(self.item_droper)

        self.attacker = Attacker(self, self.rect)
        self.components.append(self.attacker)

        self.next_moment = TimerTask(1000)
        
        self.damage_effect = DamageEffect(self.image)
        self.components.append(self.damage_effect)

        self.attack_wait = TimerTask(400)

        self.eye_rect = Rect(0, 0,1000, 1000)
        self.attack_rect = Rect(0, 0, 30, 100)

        self.hit_checker.hit_event.add_lisner(self.hit)

        self.walk_grass = []
        self.is_left = False
        self.is_walk = False

        for i in [
            "./resource/sound/walk/grass/grassWalk1.wav",
            "./resource/sound/walk/grass/grassWalk2.wav"
        ]:
            sound = SoundSource(self, i, 0, lambda dist: 0.3)
            self.walk_grass.append(sound)
            self.components.append(sound)

        self.physics.collision_enter_event.add_lisner(self.on_collison_stay)

    def on_collison_stay(self, rect, col_type):
        if self.is_walk and self.physics.on_ground:
            if col_type > 1:
                self.physics.add_force(Vector(0, 8))

    def start(self):
        super().start()
        self.player = Manger.scene.get_object("player")
    
    def update(self):
        self.eye_rect.center = self.location.world_position
        self.attack_rect.center = self.location.world_position
        self.rect.center = self.location.world_position

        if self.eye_rect.collidepoint(self.player.location.world_position):
            
            if 10 > abs(self.player.location.world_position.x - self.location.world_position.x):
                self.is_walk = False
            else:
                if self.player.location.world_position.x >= self.location.world_position.x:
                    self.is_left = False
                else:
                    self.is_left = True
            if self.attack_rect.collidepoint(self.player.location.world_position):
                self.is_walk = False
                if self.attack_wait.run_periodic_task():
                    self.attacker.hit_check(None, 2, "notliving")
            else:
                self.is_walk = True
                self.animation_manager.change_animation("walk")
            if self.is_walk:
                self.walk(self.is_left, 1, 2.5)
        else:
            if self.next_moment.run_periodic_task():
                self.next_moment.tick = int(random.random() * 1300)
                c = random.choice(move)

                if c == LivingMovements.STOP:
                    self.animation_manager.change_animation('idle')
                    self.is_walk = False
                    
                elif c == LivingMovements.WALK:
                    self.animation_manager.change_animation('walk')
                    self.is_walk = True
                    
                elif c == LivingMovements.TOGGLE:
                    self.is_left = not self.is_left

                elif c == LivingMovements.JUMP:
                    if self.physics.on_ground:
                        self.physics.add_force(Vector(0, 5))
            if self.is_walk:
                self.walk(self.is_left, 1, 1)

        self.image.set_flip(self.is_left)

    def hit(self, hiter: Attacker, status, power):
        if self.invincibility.run_periodic_task():
            self.damage_effect.reset()
            match status:
                case ItemIndex.SWORD:
                    self.heath -= int(power * 1)
                case _:
                    self.heath -= int(power * 0.6)
                    
            if self.heath < 0:
                self.item_droper.drop_item(ItemInfo(ItemIndex.SLIME_OIL, 1, None), rand=True)
                self.die_event.invoke()
                self.delete()

            self.knockback(hiter.object, Vector(3, 3))