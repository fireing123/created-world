from pygameHelper import (
    GameObject, 
    ImageObject, 
    Manger, 
    Rect,
    SoundSource,
    SoundManager
)

from pygameHelper.objects.components.physics    import physics_grounds
from components.door                            import on_broken
from components.hitObject                       import HitComponent

class CobbleWall(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name, types):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)

        cobble = Manger.tile_sheet["map"].surfaces[0]

        self.image = ImageObject(self, value=cobble, size=(1, 2))
        self.components.append(self.image)

        self.types = types

        self.rect = Rect(0, 0, 48, 96)

        self.hit_checker = HitComponent(self, self.rect)
        self.hit_checker.hit_event.add_lisner(self.attacked)
        self.components.append(self.hit_checker)
        self.hp = 5

        self.sound_manager = SoundManager({
            "stone": SoundSource(self, "./resource/sound/stone/stone.wav", 0, lambda dist: 0.6),
            "break": SoundSource(self, "./resource/sound/stone/cobbleWallBroken.wav", 0, lambda dist: 0.3)
        })

    def start(self):
        self.rect.center = self.location.world_position
        physics_grounds.append(self.rect)

    def attacked(self, hiter, status, power):
        if status in self.types:
            self.hp -= 1
            if self.hp == 0:
                self.sound_manager.play("break")
                on_broken.invoke(self.name)
                self.delete()
            else:
                self.sound_manager.play("stone")

    def delete(self):
        physics_grounds.remove(self.rect)
        return super().delete()