from pygameHelper import GameObject, SoundSource

class WaterFall(GameObject):
    def __init__(self, name, layer, tag, visible, position, rotation, parent_name):
        super().__init__(name, layer, tag, visible, position, rotation, parent_name)

        self.sound = SoundSource(self, "./resource/sound/waterfall1.wav", 0.15, lambda dist: max(-dist / 5000, -0.15))
        self.components.append(self.sound)

    def start(self):
        self.sound.play(-1)

    def update(self):
        self.sound.set_volume()
