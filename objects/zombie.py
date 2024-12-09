from pygameHelper import *

from objects.livingObject           import LivingObject

from components.inventory           import ItemIndex
from components.itemDroper          import ItemDroper
from components.hitObject           import Attacker, DamageEffect
from components.itemInfo            import ItemInfo
from components.weapon.zombiePunch  import ZombiePunch
from components.livingAI            import LivingMovements, move

import random

class Zombie(LivingObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name, 100, Rect(0, 0, 32, 64))
        self.image = ImageObject(self)
        self.components.append(self.image)

        idle_animation =    Animation(float('inf'), self.image, sheet="zombieIdle")
        walk_animation =    Animation(50,           self.image, sheet="zombieWalk")
        punch_animation =   Animation(40,           self.image, sheet="zombiePunch", once=True)
        idle_animation.change_image()

        self.animation_manager = AnimationManager(self, {
            "idle": idle_animation,
            "walk": walk_animation,
            "punch": punch_animation
        }, 'idle')

        self.components.append(self.animation_manager)

        self.punch = ZombiePunch(self)
        self.components.append(self.punch)

        self.item_droper = ItemDroper(self)
        self.components.append(self.item_droper)

        self.next_moment = TimerTask(1000)
        
        self.damage_effect = DamageEffect(self.image)
        self.components.append(self.damage_effect)

        self.attack_wait = TimerTask(1000)

        self.eye_rect = Rect(0, 0,1000, 1000)
        self.attack_rect = Rect(0, 0, 100, 100)

        self.hit_checker.hit_event.add_lisner(self.hit)

        self.is_left = False
        self.is_walk = False
            
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

        if self.eye_rect.collidepoint(self.player.location.world_position): # 플레이어가 시야 영역에 들어오면
            if self.attack_wait.not_update_run():
                if 10 > abs(self.player.location.world_position.x - self.location.world_position.x):
                    self.is_walk = False
                else:
                    if self.player.location.world_position.x >= self.location.world_position.x:
                        self.is_left = False
                    else:
                        self.is_left = True

            if self.attack_rect.collidepoint(self.player.location.world_position): # 공격 범위에 들어오면 공격
                self.is_walk = False
                if self.attack_wait.run_periodic_task():
                    self.punch.punch()
            else:
                if self.attack_wait.not_update_run():
                    self.is_walk = True
                    self.animation_manager.change_animation("walk")

            if self.is_walk and self.animation_manager.state != "punch": # 플레이어 방항으로 빠른 이동
                self.walk(self.is_left, 1, 2)
        else:
            if self.next_moment.run_periodic_task(): # 일반 ai 무빙
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
                self.item_droper.drop_item(ItemInfo(ItemIndex.ZOMBIE_BEEF, 1, None), rand=True)
                self.die_event.invoke()
                self.delete()

            self.knockback(hiter.object, Vector(3, 3))