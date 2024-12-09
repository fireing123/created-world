from pygameHelper import *

from objects.animal         import Aniaml

from components.inventory   import ItemIndex
from components.itemInfo    import ItemInfo
from components.itemDroper  import ItemDroper
from components.hitObject   import Attacker, DamageEffect
from components.livingAI    import LivingMovements, move

import random

class Chicken(Aniaml):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name, 20, Rect(0, 0, 32, 32))
        self.image = ImageObject(self)
        self.components.append(self.image)

        idle_animation = Animation(float('inf'),    self.image, sheet="chickenIdle")
        walk_animation = Animation(200,             self.image, sheet="chickenWalk")

        self.animation_manager = AnimationManager(self, {
            "idle": idle_animation,
            "walk": walk_animation
        }, "idle")

        idle_animation.change_image()
        
        self.components.append(self.animation_manager)

        self.item_droper = ItemDroper(self)
        self.components.append(self.item_droper)

        self.damage_effect = DamageEffect(self.image)
        self.components.append(self.damage_effect)

        self.hit_checker.hit_event.add_lisner(self.hit)

        self.attaked_sound = SoundSource(self, "./resource/sound/chicken/attacked/attacked.wav", 0.5, lambda dist: max(-dist / 500, -0.5))
        self.components.append(self.attaked_sound)

        self.death_sound = SoundSource(self, "./resource/sound/chicken/death/death.wav", 0.5, lambda dist: max(-dist / 500, -0.5))
        self.components.append(self.death_sound)

        self.idles = []
        for path in [
            "./resource/sound/chicken/idle/idle1.wav",
            "./resource/sound/chicken/idle/idle2.wav",
            "./resource/sound/chicken/idle/idle3.wav",
            "./resource/sound/chicken/idle/idle4.wav",
            "./resource/sound/chicken/idle/idle5.wav"
        ]:
            sound = SoundSource(self, path, 1, lambda dist: max(-dist / 250 + 0.5, -1))
            self.idles.append(sound)
            self.components.append(sound)

    def hit(self, hiter: Attacker, status, power):
        if self.invincibility.run_periodic_task():
            self.damage_effect.reset()
            self.item_droper.drop_item(ItemInfo(ItemIndex.FEATHER, int(random.random()*3), None))
            self.attaked_sound.play()
            match status:
                case ItemIndex.SWORD:
                    self.heath -= int(power * 1.5)
                case ItemIndex.ARROW:
                    self.heath -= int(power)
                    hiter.object.delete()
                case _:
                    self.heath -= int(power * 0.6)
            if self.heath < 0:
                self.item_droper.drop_item(ItemInfo(ItemIndex.CHICKEN, 1, None), rand=True)
                self.animation_manager.change_animation('idle')
                self.die_event.invoke()
                self.death_sound.play()
                self.delete()

            self.knockback(hiter.object, Vector(5, 5))
            self.runaway(hiter.object)

    def update(self):
        self.rect.center = self.location.world_position

        if self.cry_moment.run_periodic_task():
            if random.random() > 0.2:
                sound = random.choice(self.idles)
                sound.play()

        if self.next_moment.run_periodic_task():
            self.next_moment.tick = int(random.random() * 1300)
            c = random.choice(move)

            if c == LivingMovements.STOP:
                self.is_walk = False
            elif c == LivingMovements.WALK:
                self.is_walk = True
            elif c == LivingMovements.TOGGLE:
                self.is_left = not self.is_left

        self.image.set_flip(self.is_left)

        if self.is_walk:
            self.animation_manager.change_animation('walk')
            self.walk(self.is_left, 3, 1)
        else:
            self.animation_manager.change_animation('idle')