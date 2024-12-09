from pygameHelper import *

from objects.animal         import Aniaml

from components.inventory   import ItemIndex
from components.itemDroper  import ItemDroper
from components.itemInfo    import ItemInfo
from components.hitObject   import Attacker, DamageEffect
from components.livingAI    import LivingMovements, move

import random

class Cow(Aniaml):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name, 50, Rect(0, 0, 100, 50))
        self.image = ImageObject(self)
        self.components.append(self.image)

        idle_animation = Animation(float('inf'),    self.image, sheet="cowIdle")
        walk_animation = Animation(200,             self.image, sheet="cowWalk")

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

        self.attaked_sound = SoundSource(self, "./resource/sound/cow/cowHit.wav", 0, lambda dist: max(-dist / 500 + 0.2, 0))
        self.components.append(self.attaked_sound)

        self.death_sound = SoundSource(self, "./resource/sound/cow/cowDeath.wav", 0, lambda dist: max(-dist / 500 + 0.2, 0))
        self.components.append(self.death_sound)

        self.idles = []
        for path in [
            "./resource/sound/cow/cowIdle1.wav",
            "./resource/sound/cow/cowIdle2.wav"
        ]:
            sound = SoundSource(self, path, 0, lambda dist: max(-dist / 300 + 0.3, 0))
            self.idles.append(sound)
            self.components.append(sound)


    def hit(self, hiter: Attacker, status, power):
        if self.invincibility.run_periodic_task():
            self.damage_effect.reset()
            self.attaked_sound.play()
            match status:
                case ItemIndex.SWORD:
                    self.heath -= int(power * 1.5)
                case _:
                    self.heath -= int(power * 0.6)
                    
            if self.heath < 0:
                for item_index in [ItemIndex.TENDON, ItemIndex.BEEF, ItemIndex.LEATHER]:
                    self.item_droper.drop_item(ItemInfo(item_index, int(random.random()*5)+1, None), rand=True)

                self.death_sound.play()
                self.die_event.invoke()
                self.delete()

            self.knockback(hiter.object, Vector(3, 2))
            self.runaway(hiter.object)

    def update(self):
        self.rect.center = self.location.world_position

        if self.cry_moment.run_periodic_task():
            if random.random() > 0.4:
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

        self.image.set_flip(not self.is_left)

        if self.is_walk:
            self.animation_manager.change_animation('walk')
            self.walk(self.is_left, 1, 3)
        else:
            self.animation_manager.change_animation('idle')