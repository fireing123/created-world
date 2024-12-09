from pygameHelper import *

from objects.livingObject           import LivingObject

from components.inventory           import ItemIndex
from components.itemDroper          import ItemDroper
from components.hitObject           import Attacker, DamageEffect
from components.weapon.bonesBow     import BonesBow
from components.itemInfo            import ItemInfo
from components.livingAI            import LivingMovements, move

import random
import math

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.tileCollision      import CollisionTile

class Bones(LivingObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name, 60, Rect(0, 0, 32, 64))
        self.image = ImageObject(self)
        self.components.append(self.image)

        idle_animation = Animation(float('inf'),    self.image, sheet="boneIdle")
        walk_animation = Animation(50,              self.image, sheet="boneWalk")

        self.animation_manager = AnimationManager(self, {
            "idle": idle_animation,
            "walk": walk_animation,
        }, 'idle')

        idle_animation.change_image()

        self.components.append(self.animation_manager)

        self.arm = BowArm(name+"_arm", layer, "arm", [0, 7], 0, name)
        self.childrens.append(self.arm)

        self.bone_bow = BonesBow(self, self.arm)
        self.components.append(self.bone_bow)

        self.item_droper = ItemDroper(self)
        self.components.append(self.item_droper)

        self.next_moment = TimerTask(1000)
        
        self.damage_effect = DamageEffect(self.image)
        self.components.append(self.damage_effect)

        self.attack_wait = TimerTask(2500)

        self.walk_wait = TimerTask(500)

        self.eye_rect = Rect(0, 0,1500, 1500)
        self.attack_rect = Rect(0, 0, 700, 1000)
        self.back_rect = Rect(0, 0, 600, 800)

        self.hit_checker.hit_event.add_lisner(self.hit)

        self.is_left = False
        self.is_walk = False
        self.is_back = False

    def on_collison_stay(self, rect, col_type):
        if self.is_walk and self.physics.on_ground:
            if col_type > 1:
                self.physics.add_force(Vector(0, 8))


    def start(self):
        super().start()
        self.player = Manger.scene.get_object("player")
        self.tilemap: 'CollisionTile' = Manger.scene.get_object("map_renderer")
        self.arm.setup(self.player)
    
    def update(self):
        self.eye_rect.center = self.location.world_position
        self.attack_rect.center = self.location.world_position
        self.back_rect.center = self.location.world_position
        self.rect.center = self.location.world_position

        self.is_back = False
        if self.eye_rect.collidepoint(self.player.location.world_position):
            self.is_walk = True
            if self.player.location.world_position.x >= self.location.world_position.x:
                self.is_left = False
            else:
                self.is_left = True
            
            if self.attack_rect.collidepoint(self.player.location.world_position):
                if self.back_rect.collidepoint(self.player.location.world_position): 
                    self.is_back = True 
                else:
                    self.is_walk = False
                if self.attack_wait.run_periodic_task():
                    self.bone_bow.shot()

            if self.is_walk:
                is_left = not self.is_left if self.is_back else self.is_left
                self.walk(is_left, 1, 1 if self.is_back else 2)

        else:
            if self.next_moment.run_periodic_task():
                self.next_moment.tick = int(random.random() * 1300)
                c = random.choice(move)

                if c == LivingMovements.STOP:
                    self.is_walk = False
                    
                elif c == LivingMovements.WALK:
                    self.is_walk = True
                    
                elif c == LivingMovements.TOGGLE:
                    self.is_left = not self.is_left
            if self.is_walk:
                self.walk(self.is_left, 1, 1)

        if self.is_walk:
            self.animation_manager.change_animation('walk')
        else:
            self.animation_manager.change_animation('idle')

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
                self.item_droper.drop_item(ItemInfo(ItemIndex.BONE_TANK, 1, None), rand=True)
                self.die_event.invoke()
                self.delete()

            self.knockback(hiter.object, Vector(3, 3))


class BowArm(GameObject):
    def __init__(self, name, layer, tag, position, rotation, parent_name):
        super().__init__(name, layer, tag, True, position, rotation, parent_name)
        self.image = ImageObject(self)
        self.components.append(self.image)

        idle_animation = Animation(float('inf'), self.image, sheet='boneBowIdle')
        charge_animation = Animation(300, self.image, sheet='boneBowCharge', once=True)

        idle_animation.change_image()

        self.animation_manager = AnimationManager(self, {
            'idle': idle_animation,
            'charge': charge_animation
        }, 'idle')
        
        self.components.append(self.animation_manager)

        self.diretion = Vector(1, 0)

    def setup(self, player: GameObject):
        self.player = player

    def update(self):
        pos = self.player.location.world_position - self.location.world_position 
        
        time = math.sqrt(abs(pos.x))

        if time == 0:
            time = 0.1
        vx = pos.x
        vy = pos.y + time
        self.diretion = Vector(vx, vy).normalize()

        angle = Vector(0, 0).angle_to(self.diretion)
        self.location.rotation = angle
        self.location.parent.object.image.set_flip(angle > 90 or angle < -90)
