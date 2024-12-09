from pygameHelper import (
    GameObject, 
    ImageObject, 
    SoundManager, 
    SoundSource, 
    Vector
)

from objects.nomalParticle import PixelParticle

from components.hitObject import HitComponent
from components.itemDroper import ItemDroper
from components.itemInfo import ItemInfo

import random

class StoneGroup(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, random_list, allow_attackers):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)
        self.image = ImageObject(self, path="./resource/objects/stoneGroup.png", size=(3, 3))
        self.components.append(self.image)

        self.rect = self.image.og_image.get_rect()
        self.random_list = random_list

        self.hit_checker = HitComponent(self, self.rect)
        self.hit_checker.hit_event.add_lisner(self.hit)

        self.item_droper = ItemDroper(self)
        self.components.append(self.item_droper)

        self.allow_attackers = allow_attackers

        self.sound_manager = SoundManager({
            "steel": SoundSource(self, "./resource/sound/pickaxe/sword1.wav", 0, lambda dist: 0.3),
            "stone": SoundSource(self, "./resource/sound/stone/stone.wav", 0, lambda dist: 0.6)
        })

    def update(self):
        self.rect.center = self.location.world_position

    def hit(self, hiter, status, power):
        if status in self.allow_attackers:
            for i in range(6):
                particle = PixelParticle("pice", self.location.world_position, Vector(10*(0.5-random.random()), 5*(0.5-random.random())), "pixelParticles", 2)
                particle.instantiate()

            self.sound_manager.play(self.tag)
            get_item = random.choices(*self.random_list)[0]
            if get_item != None:
                self.item_droper.drop_item(ItemInfo(get_item, int(random.random()*4)+1, None), rand=True)