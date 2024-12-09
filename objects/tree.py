from pygameHelper import *

from objects.particle import Particle
from objects.nomalParticle import PixelParticle

from components.inventory import ItemIndex
from components.hitObject import HitComponent
from components.itemDroper import ItemDroper
from components.itemInfo import ItemInfo
from components.hitObject import Attacker

import random
import math

class Tree(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)

        self.image = ImageObject(self, path="./resource/objects/tree/tree_bottom.png", size=(4, 6))
        self.components.append(self.image)

        self.top = TreeUp(name+"top", layer, tag, True, [0, -110], 0, name)
        self.childrens.append(self.top)

        self.wait = OnceTimerTask(50000)
        self.wait.once = True

    def update(self):
        if self.wait.run_periodic_task():
            self.top = TreeUp(self.name+"top", self.layer, self.tag, True, [0, -110], 0, self.name)
            self.top.instantiate()

class TreeUp(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)

        self.image = ImageObject(self, path="./resource/objects/tree/tree_top.png", size=(4, 6))
        self.components.append(self.image)

        self.droper = ItemDroper(self)
        self.components.append(self.droper)

        self.rect = Rect(0, 0, 20, 288)

        self.hit_checker = HitComponent(self, self.rect)
        self.components.append(self.hit_checker)

        self.hit_checker.hit_event.add_lisner(self.drop_tree_branch)

        self.hit_count = 0

        self.wave = 0
        self.back = 0.2
        self.firction = 0.07

        self.is_living = True

        self.sound_manager = SoundManager({
            "hit": SoundSource(self, "./resource/sound/axe/axeShot.wav", 0, lambda dist: 1),
            "fall": SoundSource(self, "./resource/sound/tree/treefalling.wav", 0, lambda dist: 1),
            "break": SoundSource(self, "./resource/sound/tree/break.wav", 0, lambda dist: 1),
            "wave": SoundSource(self, "./resource/sound/tree/treewave.wav", 0, lambda dist: 1)
        })

    def start(self):
        self.rect.center = self.location.world_position

    def update(self):
        if self.is_living:
            self.wave -= self.back * self.location.rotation / 2
            self.wave += self.firction * (1 if self.wave < 0 else -1)

            if abs(self.location.rotation) < 0.2:
                self.location.rotation = 0
        else:
            self.wave += 0.005 * (1 if self.location.rotation > 0 else -1)
            if abs(self.location.rotation) > 100:
                for i in range(8):
                    self.droper.drop_item(ItemInfo(ItemIndex.TREE_BRANCH, 1, None), rand=True)
                self.location.parent.object.wait.reset()
                self.sound_manager.play("break")
                self.delete()
            
        self.location.rotation += self.wave
        
    def drop_tree_branch(self, hiter: Attacker, status, power):
        if not self.is_living: return

        match status:
            case ItemIndex.ARROW:
                return
            case ItemIndex.SWORD:
                return
            case ItemIndex.AXE:
                self.sound_manager.play("hit")
                self.hit_count += power * 2
            case _:
                self.hit_count += power

        for i in range(6):
            particle = PixelParticle("pice", self.location.world_position, Vector(10*(0.5-random.random()), 5*(0.5-random.random())), "pixelParticles", 1)
            particle.instantiate()

        if random.random() > 0.7:
            self.sound_manager.play("wave")
            for i in range(10):
                particle = LeafParticle("leaf", self.location.world_position + Vector(120*(0.5-random.random()), 200+120*(0.5-random.random())))
                particle.instantiate()

        if self.hit_count > 200:
            self.sound_manager.play("fall")
            self.is_living = False

        if self.location.world_position.x > hiter.object.location.world_position.x:
            self.wave = -1.5 if self.is_living else -0.1
        else:
            self.wave = 1.5 if self.is_living else 0.1

        if self.is_living and random.choices([True, False], [0.3, 0.7])[0]:
            self.droper.drop_item(ItemInfo(ItemIndex.TREE_BRANCH, 1, None), rand=True, pos=Vector(0, 160))

class LeafParticle(Particle):
    def __init__(self, name, position):
        super().__init__(name, position)
        self.image = ImageObject(self)
        self.components.append(self.image)

        self.animation = Animation(290, self.image, sheet="leafParticle")
        self.components.append(self.animation)
        self.create_pos = Vector(position)

        self.angle = 2.5 * random.random()
        self.fall_speed = 1
        self.swing_amplitude = 2 + 2 * (0.5 - random.random())
        self.swing_frequency = 0.05 
        self.wind_speed = 0.3 + 0.05 * (0.5 - random.random())

    def update(self):
        pos = self.location.position

        pos.y -= self.fall_speed

        self.angle += self.swing_frequency
        pos.x += math.sin(self.angle) * self.swing_amplitude

        pos.x += self.wind_speed

        self.location.position = pos

        if self.create_pos.y - 300 > self.location.position.y:
            self.delete()